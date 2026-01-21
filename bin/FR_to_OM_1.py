#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:35:07 2016

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
import os
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
y_max_max = 0

#get system basal
ask = ('Enter basal value to be substracted\nUsually:\n0 for fractional response\n1 for folds over basal')
dlg = wx.TextEntryDialog(None, ask, "Input", '0')
if dlg.ShowModal() == wx.ID_OK:
    basal = dlg.GetValue()
    basal = float(basal)
dlg.Destroy()

#define function
def func(x, Emax, pKA):
    return basal + (Emax - basal) - (((Emax-basal)*(10**x)) / (10**pKA))

#prepare file for writing results
if os.path.isfile("FR_to_OM.res"):
    os.remove("FR_to_OM.res")
res = open("FR_to_OM.res","w")
res.write("Meta-analysis: FR to OM\n\n")
res.write("# Emax\tlogKa\tbasal\tData file\n")
#prepare file for Grace plot
if os.path.isfile("FR_to_OM.draw"):
    os.remove("FR_to_OM.draw")
draw = open("FR_to_OM.draw","w")
c=-1 #plot counter
d=0 #symbolcounter

#first data set
dialog = wx.FileDialog(None, "Choose dat file to be analysed.", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected_1=dialog.GetPath()
    data_1 = np.loadtxt(selected_1)    
    columns = np.size((data_1)[0,:])
#test wheter we have data
if columns == 0:
    msg = ('Empty data file\n')
    errors = msg
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
else:
    # load data
    data = np.loadtxt(selected_1)
    x_data = data[:,0]
    y_data = data[:,1]
    x_data_err = data[:,2]
    y_data_err = data[:,3]
    x_min = np.amin(x_data)
    x_max = np.amax(x_data)
    y_min = np.amin(y_data)
    y_max = np.amax(y_data)
    if np.size(x_data) < 4:
        msg = ('Too few data points in ' +str(selected_1)+ ' This data will be skipped\n')
        err = err + msg
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    else:
        if x_min < -15 or x_max > 0:
            msg = ('X value out of range ,<15,0>! '+str(selected_1)+' will be skipped\n')
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
            #get estimates & bounds
            Emax_estim = y_max
            Emax_min = y_max * 0.5
            Emax_max = y_max * 10
            pKA_estim = x_max + 0.5
            pKA_min = x_max
            pKA_max = x_max + 3
            #get basal value
            #fit data
            p0 = np.array([Emax_estim, pKA_estim])
            popt, pcov = opt.curve_fit(func, x_data, y_data, p0, bounds=([Emax_min, pKA_min],[Emax_max, pKA_max]))
            perr = np.sqrt(np.diag(pcov))
            Emax_calc = (popt[0])
            pKA_calc = (popt[1])
            Emax_err = (perr[0])
            pKA_err = (perr[1])
            #write results
            head, tail = os.path.split(selected_1)
            Emax_res = (str("{0:.2f}".format(Emax_calc))+' ± '+str("{0:.2f}".format(Emax_err)))
            pKA_res = (str("{0:.2f}".format(pKA_calc))+' ± '+str("{0:.2f}".format(pKA_err)))
            res.write(str(Emax_res)+"\t"+str(pKA_res)+"\t"+str(basal)+"\t"+str(tail)+"\n")
            #write Grace plot
            c=(c+1)
            d=(d+1)
            draw.write("read xydxdy \""+str(selected_1)+"\" \n")
            draw.write("s"+str(c)+" symbol "+str(d)+" \n")
            draw.write("s"+str(c)+" symbol size 0.8 \n")
            draw.write("s"+str(c)+" symbol color 1 \n")
            draw.write("s"+str(c)+" symbol fill color 0 \n")
            draw.write("s"+str(c)+" symbol fill pattern 1 \n")
            draw.write("s"+str(c)+" errorbar color 1 \n")
            draw.write("s"+str(c)+" errorbar size 0.8 \n")
            draw.write("s"+str(c)+" line type 0 \n")
            draw.write("s"+str(c)+" legend \"E\\sMAX\\N="+str("{0:.2f}".format(Emax_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax_err))+"; logK\\sA\\N="+str("{0:.2f}".format(pKA_calc))+' \\#{B1} '+str("{0:.2f}".format(pKA_err))+"; basal= "+str(basal)+"; "+str(tail)+"\" \n")
            #calculate fit
            y_fit = func(x_data, *popt)
            xy_fit = np.column_stack((x_data, y_fit))
            #save fit
            fit=(str(tail)+'_FR_to_OM_1_fit.data')
            np.savetxt(fit,xy_fit,fmt='%.4e')
            #calculate curve
            x_curve = np.arange(x_min, x_max, step)
            y_curve = func(x_curve, *popt)
            xy_curve = np.column_stack((x_curve, y_curve))
            #save curve
            curve=(str(tail)+'_FR_to_OM_1_curve.data')
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
plt.title("Meta-analysis")
plt.axis([ax_min,ax_max,0,ay_max])
plt.xlabel("pEC50")
plt.ylabel("Emax")
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
draw.write("xaxis label \"pEC\\s50\\N\"  \n")
draw.write("xaxis label font \"Helvetica\"  \n")
draw.write("xaxis ticklabel font \"Helvetica\"  \n")
draw.write("xaxis  tick major 1 \n")
draw.write("xaxis  tick major size 0.8 \n")
draw.write("xaxis  tick minor size 0.4 \n")
draw.write("yaxis label \"E\\sMAX\\N\"  \n")
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
