#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:35:07 2016

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
import glob,os
import sys
import subprocess
import time
import wx
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

#color list
color_list = np.array(['k','b','r','g','c','m','y'])

#error log
if os.path.isfile("temp.log"):
    os.remove("temp.log")
err = ''

#initialize counters
i = -1
x_min_min = 0
x_max_max = -15

#test wheter we have files
count = len(glob.glob('*.dat'))
if count == 0:
    msg = ('No .dat files found!\n')
    err = msg
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
else:
    #prepare file for writing results
    if os.path.isfile("competition_1.res"):
        os.remove("competition_1.res")
    res = open("competition_1.res","w")
    res.write("Single site competition\n")
    res.write("logIC50\t\tnH\t\t\tData file\n")
    #prepare file for Grace plot
    if os.path.isfile("comp_1.draw"):
        os.remove("comp_1.draw")
    draw = open("comp_1.draw","w")
    c=-1 #plot counter
    d=0 #symbolcounter
    
    for file in sorted(glob.glob('*.dat')):
        if file == '':
          exit()
        # load data
        data = np.loadtxt(file)
        x_data = data[:,0]
        y_data = data[:,1]
        y_data_err = data[:,2]
        x_min = np.amin(x_data)
        x_max = np.amax(x_data)
        y_min = np.amin(y_data)
        y_max = np.amax(y_data)
        if np.size(x_data) < 6 or (x_max - x_min) < 3:
            msg = ('Too few data points in ' +str(file)+ ' This data will be skipped\n')
            err = err + msg
            dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            if x_min < -15 or x_max > 0:
                msg = ('X value out of range ,<15,0>! '+str(file)+' will be skipped\n')
                err = err + msg
                dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
                dialog.ShowModal()
                dialog.Destroy()
            else:
                if x_max > x_max_max:
                    x_max_max = x_max
                if x_min < x_min_min:
                    x_min_min = x_min
                step = (x_max - x_min) * 0.01
                #get estimates & bounds
                nH_estim = 1
                nH_min = 0.5
                nH_max = 2
                IC50_estim = (x_min + x_max) /2
                IC50_min = x_min
                IC50_max = x_max
                #fit data
                p0 = np.array([IC50_estim, nH_estim])
                def func(x, IC50, nH):
                    global nH_estim, nH_min, nH_max
                    nH_estim = float(nH_estim)
                    nH_min = float(nH_min)
                    nH_max = float(nH_max)
                    return 100 - 100*10**(x*nH) / (10**(IC50*nH) + 10**(x*nH))
                popt, pcov = opt.curve_fit(func, x_data, y_data, p0, bounds=([IC50_min,nH_min],[IC50_max,nH_max]))
                perr = np.sqrt(np.diag(pcov))
                IC50_calc = (popt[0])
                nH_calc = (popt[1])
                IC50_err = (perr[0])
                nH_err = (perr[1])
                #write results
                IC50_res = (str("{0:.2f}".format(IC50_calc))+' ± '+str("{0:.2f}".format(IC50_err)))
                nH_res = (str("{0:.2f}".format(nH_calc))+' ± '+str("{0:.2f}".format(nH_err)))
                res.write(str(IC50_res)+"\t"+str(nH_res)+"\t"+str(file)+"\n")
                #write Grace plot
                c=(c+1)
                d=(d+1)
                base=os.path.splitext(file)[0]
                draw.write("read xydy \""+str(file)+"\" \n")
                draw.write("s"+str(c)+" symbol "+str(d)+" \n")
                draw.write("s"+str(c)+" symbol size 0.8 \n")
                draw.write("s"+str(c)+" symbol color "+str(d)+" \n")
                draw.write("s"+str(c)+" symbol fill color "+str(d)+" \n")
                draw.write("s"+str(c)+" symbol fill pattern 1 \n")
                draw.write("s"+str(c)+" errorbar color "+str(d)+" \n")
                draw.write("s"+str(c)+" errorbar size 0.8 \n")
                draw.write("s"+str(c)+" line type 0 \n")
                draw.write("s"+str(c)+" legend \"log IC\\s50\\N="+str("{0:.2f}".format(IC50_calc))+' \\#{B1} '+str("{0:.2f}".format(IC50_err))+"; n\\H\\N="+str("{0:.2f}".format(nH_calc))+' \\#{B1} '+str("{0:.2f}".format(nH_err))+"; "+str(base)+"\" \n")
                #calculate curve
                x_calc = np.arange(x_min, x_max, step)
                y_calc = func(x_calc, *popt)
                xy_calc = np.column_stack((x_calc, y_calc))
                #save fit curve
                c=(c+1)
                e=(c-1)
                fit=(str(base)+'_comp_1_fit.data')
                draw.write("read xy \""+str(fit)+"\" \n")
                draw.write("s"+str(c)+" symbol 0 \n")
                draw.write("s"+str(c)+" line type 1 \n")
                draw.write("s"+str(c)+" line color "+str(d)+" \n")
                draw.write("s"+str(c)+" layer 51 \n")
                draw.write("s"+str(c)+" legend off \n")
                np.savetxt(fit,xy_calc,fmt='%.4e')
                #get color
                i = i + 1
                if i == 7:
                    msg = ("More than 7 data sets. Colors repeat.\n")
                    err = err + msg
                    dialog = wx.MessageDialog(None, msg, 'Warning', wx.OK)
                    dialog.ShowModal()
                    dialog.Destroy()
                    i = i - 7
                color = (color_list[i])
                # plot
                plt.plot(x_calc, y_calc, color)
                plt.errorbar(x_data, y_data, xerr=None, yerr=y_data_err, fmt = color + "o")
    
    now = time.strftime("%d.%m.%Y %H:%M:%S")
    res.write("\n\n"+str(now)+"\n")
    res.close()
    #Plot
    ax_min = x_min_min - 0.5
    ax_max = x_max_max + 0.5
    plt.title("Competition binding")
    plt.axis([ax_min,ax_max,0,120])
    plt.xlabel("ligand [log c]")
    plt.ylabel("tracer binding [% of control]")
    plt.show()
    #Grace plot
    draw.write("page size 595, 842 \n")
    draw.write("view xmin 0.2 \n")
    draw.write("view xmax 0.8 \n")
    draw.write("view ymin 0.85 \n")
    draw.write("view ymax 1.25 \n")
    draw.write("world xmin "+str(ax_min)+" \n")
    draw.write("world xmax "+str(ax_max)+" \n")
    draw.write("world ymin 0 \n")
    draw.write("world ymax 120 \n")
    draw.write("xaxis label \"[log c]\"  \n")
    draw.write("xaxis label font \"Helvetica\"  \n")
    draw.write("xaxis ticklabel font \"Helvetica\"  \n")
    draw.write("xaxis  tick major 1 \n")
    draw.write("xaxis  tick major size 0.8 \n")
    draw.write("xaxis  tick minor size 0.4 \n")
    draw.write("yaxis label \"binding [% of control]\"  \n")
    draw.write("yaxis label font \"Helvetica\"  \n")
    draw.write("yaxis ticklabel font \"Helvetica\"  \n")
    draw.write("yaxis  tick major size 0.8 \n")
    draw.write("yaxis  tick minor size 0.4 \n")
    draw.write("legend 0.08, 0.7 \n")
    draw.write("legend char size 0.8 \n")
    draw.write("legend font \"Helvetica\" \n")
    draw.close()

log = open("temp.log","w")
log.write(err)
log.close()
