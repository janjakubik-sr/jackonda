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
x_min_min = 0
x_max_max = -15
y_max_max = 1

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
    if os.path.isfile("FR_OM_3.res"):
        os.remove("FR_OM_3.res")
    res = open("FR_OM_3.res","w")
    res.write("Functional response - Operational Model\nNo global fit will be performed\n\n")
    res.write("# tau\tlogKA\tEmax\tbasal\tData file\n")
    #prepare file for Grace plot
    if os.path.isfile("FR_OM_3.draw"):
        os.remove("FR_OM_3.draw")
    draw = open("FR_OM_3.draw","w")
    c=-1 #plot counter
    d=0  #symbolcounter
    #get system Emax
    ask = ('Enter system Emax \n')
    dlg = wx.TextEntryDialog(None, ask, "Input",'1')
    if dlg.ShowModal() == wx.ID_OK:
        global Emax
        Emax = dlg.GetValue()
        Emax = float(Emax)
    dlg.Destroy()
    #get system basal
    ask = ('Enter system basal. Usually:\n0 for fractional response\n1 for fold over basal')
    dlg = wx.TextEntryDialog(None, ask, "Input",'0')
    if dlg.ShowModal() == wx.ID_OK:
        global basal
        basal = dlg.GetValue()
        basal = float(basal)
    dlg.Destroy()
    
    #initial best fit
    i = -1
    res.write("\nIndividual best fits\n")
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
        #get value of logKA
        ask = ('Enter logKA of agonist for '+str(file)+' \n')
        dlg = wx.TextEntryDialog(None, ask, "Input",'-6')
        if dlg.ShowModal() == wx.ID_OK:
            global pKA
            pKA = dlg.GetValue()
            pKA = float(pKA)
        dlg.Destroy()
        if np.size(x_data) < 5 or (x_max - x_min) < 2.5:
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
                if y_max > y_max_max:
                    y_max_max = y_max
                step = (x_max - x_min) * 0.01
                #calculate estimates
                if y_max > (0.98*Emax):
                    tau_estim = 1000
                else:
                    tau_estim = (1 / ((Emax - basal) / (y_max - basal) -1))
                tau_min = tau_estim / 10
                tau_max = tau_estim * 10
                #fit data
                p0 = np.array([tau_estim])
                def func(x, tau):
                    return basal + ((10**x) * tau * (Emax - basal)) / ((10**x) * (1 +tau) + (10**pKA))
                popt, pcov = opt.curve_fit(func, x_data, y_data, p0, bounds=([tau_min],[tau_max]))
                perr = np.sqrt(np.diag(pcov))
                tau_calc = (popt[0])
                tau_err = (perr[0])
                #write results
                tau_res = (str("{0:.4f}".format(tau_calc))+' ± '+str("{0:.4f}".format(tau_err)))
                res.write(str(tau_res)+"\t"+str(pKA)+"\t"+str(Emax)+"\t"+str(basal)+"\t"+str(file)+"\n")
                #write Grace plot
                c=(c+1)
                d=(d+1)
                base=os.path.splitext(file)[0]
                draw.write("read xydy \""+str(file)+"\" \n")
                draw.write("s"+str(c)+" symbol "+str(d)+" \n")
                draw.write("s"+str(c)+" symbol size 0.8 \n")
                draw.write("s"+str(c)+" symbol color 1 \n")
                draw.write("s"+str(c)+" symbol fill color 0 \n")
                draw.write("s"+str(c)+" symbol fill pattern 1 \n")
                draw.write("s"+str(c)+" errorbar color 1 \n")
                draw.write("s"+str(c)+" errorbar size 0.8 \n")
                draw.write("s"+str(c)+" line type 0 \n")
                draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau_calc))+' \\#{B1} '+str("{0:.4f}".format(tau_err))+"; logK\\sA\\N ="+str("{0:.2f}".format(pKA))+"; E\\sMAX\\N = "+str("{0:.2f}".format(Emax))+"; basal = "+str("{0:.2f}".format(basal))+"; "+str(base)+"\" \n")
                #calculate fit
                y_fit = func(x_data, *popt)
                xy_fit = np.column_stack((x_data, y_fit))
                #save fit
                fit=(str(base)+'_FR_OM_3_fit.data')
                np.savetxt(fit,xy_fit,fmt='%.4e')
                #calculate curve
                x_curve = np.arange(x_min, x_max, step)
                y_curve = func(x_curve, *popt)
                xy_curve = np.column_stack((x_curve, y_curve))
                #save curve
                curve=(str(base)+'_FR_OM_3_curve.data')
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
    ax_min = x_min_min - 0.5
    ax_max = x_max_max + 0.5
    ay_max = y_max_max * 1.1
    plt.title("Functional response")
    plt.axis([ax_min,ax_max,0,ay_max])
    plt.xlabel("ligand [log c]")
    plt.ylabel("response [fold over basal]")
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
    draw.write("world ymax "+str(ay_max)+" \n")
    draw.write("xaxis label \"[log c]\"  \n")
    draw.write("xaxis label font \"Helvetica\"  \n")
    draw.write("xaxis ticklabel font \"Helvetica\"  \n")
    draw.write("xaxis  tick major 1 \n")
    draw.write("xaxis  tick major size 0.8 \n")
    draw.write("xaxis  tick minor size 0.4 \n")
    draw.write("yaxis label \"[fold over basal]\"  \n")
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
