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
x_max_max = 0

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
    if os.path.isfile("dissociation_2.res"):
        os.remove("dissociation_2.res")
    res = open("dissociation_2.res","w")
    res.write("Dissociation from two sites\n\n")
    res.write("Koff1\t\t\tKoff2\t\t\tF2\t\t\tData file\n")
    #prepare file for Grace plot
    if os.path.isfile("dissoc_2.draw"):
        os.remove("dissoc_2.draw")
    draw = open("dissoc_2.draw","w")
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
        if np.size(x_data) < 8:
            msg = ('Too few data points in ' +str(file)+ ' This data will be skipped\n')
            err = err + msg
            dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            if x_min < 0 or y_max < 0 or y_max > 120:
                msg = ('Wrong data! Probably not normalized.\n'+str(file)+' will be skipped\n')
                err = err + msg
                dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
                dialog.ShowModal()
                dialog.Destroy()
            else:
                if x_max > x_max_max:
                    x_max_max = x_max
                step = (x_max - x_min) * 0.01
                #get estimates & bounds
                Koff1_estim = 0.693 / (x_max * 0.3)
                Koff1_min = 0.693 / x_max
                Koff1_max = 0.693 / (x_max * 0.03)
                Koff2_estim = 0.693 / (x_max * 0.6)
                Koff2_min = 0.693 / (x_max * 2)
                Koff2_max = 0.693 / (x_max * 0.3)
                F2_estim = 50
                F2_min = 0
                F2_max = 100
                #fit data
                p0 = np.array([Koff1_estim, Koff2_estim, F2_estim])
                def func(x, Koff1, Koff2, F2):
                    import numpy
                    return (100 - F2) * numpy.exp(-Koff1 * x) + F2 * numpy.exp(-Koff2 * x)
                popt, pcov = opt.curve_fit(func, x_data, y_data, p0, bounds=([Koff1_min, Koff2_min, F2_min],[Koff1_max, Koff2_max, F2_max]))
                perr = np.sqrt(np.diag(pcov))
                Koff1_calc = (popt[0])
                Koff1_err = (perr[0])
                Koff2_calc = (popt[1])
                Koff2_err = (perr[1])
                F2_calc = (popt[2])
                F2_err = (perr[2])
                #write results
                Koff1_res = (str("{0:.4f}".format(Koff1_calc))+' ± '+str("{0:.4f}".format(Koff1_err)))
                Koff2_res = (str("{0:.4f}".format(Koff2_calc))+' ± '+str("{0:.4f}".format(Koff2_err)))
                F2_res = (str("{0:.0f}".format(F2_calc))+' ± '+str("{0:.0f}".format(F2_err)))
                res.write(str(Koff1_res)+"\t"+str(Koff2_res)+"\t"+str(F2_res)+"\t\t"+str(file)+"\n")
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
                draw.write("s"+str(c)+" legend \"K\\sOff1\\N="+str("{0:.4f}".format(Koff1_calc))+' \\#{B1} '+str("{0:.4f}".format(Koff1_err))+"; K\\sOff2\\N="+str("{0:.4f}".format(Koff2_calc))+' \\#{B1} '+str("{0:.4f}".format(Koff2_err))+"; F\\s2\\N="+str("{0:.0f}".format(F2_calc))+' \\#{B1} '+str("{0:.0f}".format(F2_err))+"; "+str(base)+"\" \n")
                #calculate fit
                y_fit = func(x_data, *popt)
                xy_fit = np.column_stack((x_data, y_fit))
                #save fit
                fit=(str(base)+'_dissoc_2_fit.data')
                np.savetxt(fit,xy_fit,fmt='%.4e')
                #calculate curve
                x_curve = np.arange(0, x_max, step)
                y_curve = func(x_curve, *popt)
                xy_curve = np.column_stack((x_curve, y_curve))
                #save curve
                curve=(str(base)+'_dissoc_2_curve.data')
                np.savetxt(curve,xy_curve,fmt='%.4e')
                c=(c+1)
                e=(c-1)
                draw.write("read xy \""+str(curve)+"\" \n")
                draw.write("s"+str(c)+" symbol 0 \n")
                draw.write("s"+str(c)+" line type 1 \n")
                draw.write("s"+str(c)+" line color "+str(d)+" \n")
                draw.write("s"+str(c)+" layer 51 \n")
                draw.write("s"+str(c)+" legend off \n")
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
                plt.plot(x_curve, y_curve, color)
                plt.errorbar(x_data, y_data, xerr=None, yerr=y_data_err, fmt = color + "o")
    
    now = time.strftime("%d.%m.%Y %H:%M:%S")
    res.write("\n\n"+str(now)+"\n")
    res.close()
    #Plot
    ax_max = x_max_max * 1.1
    plt.title("Binding kinetics")
    plt.axis([0,ax_max,0,120])
    plt.xlabel("Time [min]")
    plt.ylabel("tracer binding [% of control]")
    plt.show()
    #Grace plot
    draw.write("page size 595, 842 \n")
    draw.write("view xmin 0.2 \n")
    draw.write("view xmax 0.8 \n")
    draw.write("view ymin 0.85 \n")
    draw.write("view ymax 1.25 \n")
    draw.write("world xmin 0 \n")
    draw.write("world xmax "+str(ax_max)+" \n")
    draw.write("world ymin 0 \n")
    draw.write("world ymax 120 \n")
    draw.write("xaxis label \"Time []\"  \n")
    draw.write("xaxis label font \"Helvetica\"  \n")
    draw.write("xaxis ticklabel font \"Helvetica\"  \n")
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
