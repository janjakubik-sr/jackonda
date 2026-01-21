#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:35:07 2016

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
import glob,os
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
y_max_max = 0

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
    if os.path.isfile("saturation_1.res"):
        os.remove("saturation_1.res")
    res = open("saturation_1.res","w")
    res.write("Saturation of a single site\n\n")
    res.write("Bmax\t\tKD\t\t\t\tData file\n")
    #prepare file for Grace plot
    if os.path.isfile("satur_1.draw"):
        os.remove("satur_1.draw")
    draw = open("satur_1.draw","w")
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
        if np.size(x_data) < 5:
            msg = ('Too few data points in ' +str(file)+ ' This data will be skipped\n')
            err = err + msg
            dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            if x_min < 0:
                msg = ('Negative x value found found! '+str(file)+' will be skipped\n')
                err = err + msg
                dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
                dialog.ShowModal()
                dialog.Destroy()
            else:
                x_max = np.amax(x_data)
                if x_max > x_max_max:
                    x_max_max = x_max
                y_max = np.amax(y_data)
                if y_max > y_max_max:
                    y_max_max = y_max
                step = x_max / 100
                #get estimates & bounds
                KD_estim = x_max * 0.5
                KD_min = 0
                KD_max = x_max
                Bmax_estim = y_max
                Bmax_min = 0
                Bmax_max = 2 * y_max
                #fit data
                p0 = np.array([Bmax_estim, KD_estim])
                def func(x, Bmax, KD):
                    return Bmax*x / (KD + x)
                popt, pcov = opt.curve_fit(func, x_data, y_data, p0, bounds=([Bmax_min,KD_min],[Bmax_max,KD_max]))
                perr = np.sqrt(np.diag(pcov))
                Bmax_calc = (popt[0])
                KD_calc = (popt[1])
                Bmax_err = (perr[0])
                KD_err = (perr[1])
                #write results
                Bmax_res = (str("{0:.2f}".format(Bmax_calc))+' ± '+str("{0:.2f}".format(Bmax_err)))
                KD_res = (str("{0:.2f}".format(KD_calc))+' ± '+str("{0:.2f}".format(KD_err)))
                res.write(str(Bmax_res)+"\t"+str(KD_res)+"\t"+str(file)+"\n")
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
                draw.write("s"+str(c)+" legend \"K\\sD\\N="+str("{0:.2f}".format(KD_calc))+' \\#{B1} '+str("{0:.2f}".format(KD_err))+"; B\\sMAX\\N="+str("{0:.2f}".format(Bmax_calc))+' \\#{B1} '+str("{0:.2f}".format(Bmax_err))+"; "+str(base)+"\" \n")
                #calculate fit
                y_fit = func(x_data, *popt)
                xy_fit = np.column_stack((x_data, y_fit))
                #save fit
                fit=(str(base)+'_satur_1_fit.data')
                np.savetxt(fit,xy_fit,fmt='%.4e')
                #calculate curve
                x_curve = np.arange(0, x_max, step)
                y_curve = func(x_curve, *popt)
                xy_curve = np.column_stack((x_curve, y_curve))
                #save curve
                curve=(str(base)+'_satur_1_curve.data')
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
    ay_max = y_max_max * 1.2
    plt.title("Saturation binding")
    plt.axis([0,ax_max,0,ay_max])
    plt.xlabel("Free")
    plt.ylabel("Bound")
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
    draw.write("world ymax "+str(ay_max)+" \n")
    draw.write("xaxis label \"Free [ ]\"  \n")
    draw.write("xaxis label font \"Helvetica\"  \n")
    draw.write("xaxis ticklabel font \"Helvetica\"  \n")
    draw.write("xaxis  tick major size 0.8 \n")
    draw.write("xaxis  tick minor size 0.4 \n")
    draw.write("yaxis label \"binding [pmol / mg of protein]\"  \n")
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
