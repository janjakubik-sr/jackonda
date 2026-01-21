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
x_min_min = 0
x_max_max = -15
y_max_max = 100

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
    if os.path.isfile("dualsteric.res"):
        os.remove("dualsteric.res")
    res = open("dualsteric.res","w")
    res.write("Dualsteric interaction\n\n")
    res.write("logKA\t\t\talpha\t\tlogKB\t\tKD\t\t[X]\t\tData file\n")
    #prepare file for Grace plot
    if os.path.isfile("dualster.draw"):
        os.remove("dualster.draw")
    draw = open("dualster.draw","w")
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
        if np.size(x_data) < 5 or (x_max - x_min) < 3:
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
                if y_max > y_max_max:
                    y_max_max = y_max
                if x_max > x_max_max:
                    x_max_max = x_max
                if x_min < x_min_min:
                    x_min_min = x_min
                step = (x_max - x_min) * 0.01
                #get estimates & bounds
                if y_max > 105:
                    alpha_estim = 3
                    alpha_min = 1.1
                    alpha_max = 1000
                else:
                    alpha_estim = 0.5
                    alpha_min = 0.001
                    alpha_max = 0.9
                KA_estim = (x_min + x_max) * 0.6
                KA_min = x_min
                KA_max = x_max
                KB_estim = (x_min + x_max) * 0.3
                KB_min = x_min
                KB_max = x_max              
                #get tracer KD and concentration
                ask = ('Enter KD value for ' +str(file)+'\n')
                dlg = wx.TextEntryDialog(None, ask,"Input","250e-12")
                if dlg.ShowModal() == wx.ID_OK:
                    KD = dlg.GetValue()
                dlg.Destroy()
                ask = ('Enter tracer concentration for ' +str(file)+'\n')
                dlg = wx.TextEntryDialog(None, ask,"Input","100e-12")
                if dlg.ShowModal() == wx.ID_OK:
                    CX = dlg.GetValue()
                dlg.Destroy()            
                #fit data
                p0 = np.array([KA_estim, alpha_estim, KB_estim])
                def func(x, KA, alpha, KB):
                    global CX
                    CX = float(CX)
                    global KD
                    KD = float(KD)
                    return 100 * (CX + KD) / (CX + (KD * ((10**x)*(10**KB + (10**x))+10**KA*(10**KB+(10**x))))/(10**KB*(10**KA + (10**x)*alpha)))
                popt, pcov = opt.curve_fit(func, x_data, y_data, p0, bounds=([KA_min,alpha_min,KB_min],[KA_max,alpha_max,KB_max]))
                perr = np.sqrt(np.diag(pcov))
                KA_calc = (popt[0])
                alpha_calc = (popt[1])
                KB_calc = (popt[2])
                KA_err = (perr[0])
                alpha_err = (perr[1])
                KB_err = (perr[2])
                #write results
                KA_res = (str("{0:.2f}".format(KA_calc))+' ± '+str("{0:.2f}".format(KA_err)))
                if alpha_calc > 1:
                    alpha_res = (str("{0:.2f}".format(alpha_calc))+' ± '+str("{0:.2f}".format(alpha_err)))
                else:
                    alpha_res = (str("{0:.4f}".format(alpha_calc))+' ± '+str("{0:.4f}".format(alpha_err)))
                KB_res = (str("{0:.2f}".format(KB_calc))+' ± '+str("{0:.2f}".format(KB_err)))
                res.write(str(KA_res)+"\t"+str(alpha_res)+"\t"+str(KB_res)+"\t"+str(KD)+"\t"+str(CX)+"\t"+str(file)+"\n")
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
                if alpha_calc > 1:
                    draw.write("s"+str(c)+" legend \"logK\\sA\\N="+str("{0:.2f}".format(KA_calc))+" \\#{B1} "+str("{0:.2f}".format(KA_err))+"; \\f{Symbol}a\\f{}="+str("{0:.2f}".format(alpha_calc))+" \\#{B1} "+str("{0:.2f}".format(alpha_err))+"; logK\\sB\\N="+str("{0:.2f}".format(KB_calc))+" \\#{B1} "+str("{0:.2f}".format(KB_err))+"; "+str(base)+"\" \n")
                else:
                    draw.write("s"+str(c)+" legend \"logK\\sA\\N="+str("{0:.2f}".format(KA_calc))+" \\#{B1} "+str("{0:.2f}".format(KA_err))+"; \\f{Symbol}a\\f{}="+str("{0:.4f}".format(alpha_calc))+" \\#{B1} "+str("{0:.4f}".format(alpha_err))+"; logK\\sB\\N="+str("{0:.2f}".format(KB_calc))+" \\#{B1} "+str("{0:.2f}".format(KB_err))+"; "+str(base)+"\" \n")
                #calculate fit
                y_fit = func(x_data, *popt)
                xy_fit = np.column_stack((x_data, y_fit))
                #save fit
                fit=(str(base)+'_dualster_fit.data')
                np.savetxt(fit,xy_fit,fmt='%.4e')
                #calculate curve
                x_curve = np.arange(x_min, x_max, step)
                y_curve = func(x_curve, *popt)
                xy_curve = np.column_stack((x_curve, y_curve))
                #save curve
                curve=(str(base)+'_dualster_curve.data')
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
    plt.title("Dualsteric interaction")
    plt.axis([ax_min,ax_max,0,ay_max])
    plt.xlabel("dualsteric modulator [log c]")
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
    draw.write("world ymax "+str(ay_max)+" \n")
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
    draw.write("legend 0.15, 0.7 \n")
    draw.write("legend char size 0.8 \n")
    draw.write("legend font \"Helvetica\" \n")
    draw.close()

log = open("temp.log","w")
log.write(err)
log.close()
