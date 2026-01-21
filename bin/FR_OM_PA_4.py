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
errors = ''

#initialize counters
x_min_min = 0
x_max_max = -15
y_max_max = 1

#Get system basal
ask = ('Enter system basal. Usually:\n0 for fractional response\n1 for fold over basal')
dlg = wx.TextEntryDialog(None, ask, "Input",'0')
if dlg.ShowModal() == wx.ID_OK:
    global basal
    basal = float(dlg.GetValue())
dlg.Destroy()

#Full agonist best fit
#select file
dialog = wx.FileDialog(None, "Choose dat file of full agonist", os.getcwd(), "","*.dat", wx.FD_OPEN)
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
    #prepare file for writing results
    path_1, file_1=os.path.split(selected_1)
    base_1=os.path.splitext(selected_1)[0]
    if os.path.isfile("FR_OM_PA.res"):
        os.remove("FR_OM_PA.res")
    res = open("FR_OM_PA.res","w")
    res.write("Functional response - Operational Model - Partial agonist\n\n")
    res.write("# tau\tEmax\tpKA\tData file\n")
    #prepare file for Grace plot
    if os.path.isfile("FR_OM_PA.draw"):
        os.remove("FR_OM_PA.draw")
    draw = open("FR_OM_PA.draw","w")
    c=-1 #plot counter
    d=0  #symbolcounter
    #initial best fit for full agonist
    i = -1
    res.write("\nfull agonist\n")
    # load data
    x_data_1 = data_1[:,0]
    y_data_1 = data_1[:,1]
    y_data_err_1 = data_1[:,2]
    x_min = np.amin(x_data_1)
    x_max = np.amax(x_data_1)
    y_min = np.amin(y_data_1)
    y_max = np.amax(y_data_1)
    if np.size(x_data_1) < 5 or (x_max - x_min) < 2.5:
        msg = ('Too few data points in ' +str(file_1)+ ' This data will be skipped\n')
        errors = errors + msg
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    else:
        if x_min < -15 or x_max > 0:
            msg = ('X value out of range ,<15,0>! '+str(file_1)+' will be skipped\n')
            errors = errors + msg
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
            Emax1_estim = basal + (y_max - basal) * 2
            Emax1_min = basal + (Emax1_estim - basal) * 0.1
            Emax1_max = basal + (Emax1_estim - basal) * 10
            tau1_estim = 1
            tau1_min = 0.001
            tau1_max = 1000
            #Get agonist affinity
            ask = ('Enter pKA of agonist for '+str(file_1)+'\n')
            dlg = wx.TextEntryDialog(None, ask, "Input",'-6')
            if dlg.ShowModal() == wx.ID_OK:
                pKA1 = float(dlg.GetValue())
            dlg.Destroy()
            p1 = [tau1_estim, Emax1_estim]
            #fit data
            def func(x, tau1, Emax1):
                return basal + ((10**x) * tau1 * (Emax1 - basal)) / ((10**x) * (1 +tau1) + (10**pKA1))
            p1_opt, p1_cov = opt.curve_fit(func, x_data_1, y_data_1, p1, bounds=([tau1_min, Emax1_min],[tau1_max,Emax1_max]))
            p1_err = np.sqrt(np.diag(p1_cov))
            tau1_calc = (p1_opt[0])
            Emax1_calc = (p1_opt[1])
            tau1_err = (p1_err[0])
            Emax1_err = (p1_err[1])
            #write results
            tau1_res = (str("{0:.4f}".format(tau1_calc))+' ± '+str("{0:.4f}".format(tau1_err)))
            Emax1_res = (str("{0:.2f}".format(Emax1_calc))+' ± '+str("{0:.2f}".format(Emax1_err)))
            res.write(str(tau1_res)+"\t"+str(Emax1_res)+"\t"+str(pKA1)+"\t"+str(file_1)+"\n")
            #write Grace plot
            c=(c+1)
            d=(d+1)
            draw.write("read xydy \""+str(file_1)+"\" \n")
            draw.write("s"+str(c)+" symbol "+str(d)+" \n")
            draw.write("s"+str(c)+" symbol size 0.8 \n")
            draw.write("s"+str(c)+" symbol color 1 \n")
            draw.write("s"+str(c)+" symbol fill color 0 \n")
            draw.write("s"+str(c)+" symbol fill pattern 1 \n")
            draw.write("s"+str(c)+" errorbar color 1 \n")
            draw.write("s"+str(c)+" errorbar size 0.8 \n")
            draw.write("s"+str(c)+" line type 0 \n")
            draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau1_calc))+' \\#{B1} '+str("{0:.4f}".format(tau1_err))+"; E\\sMAX\\N="+str("{0:.2f}".format(Emax1_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax1_err))+"; pK\\sA\\N="+str("{0:.2f}".format(pKA1))+"; "+str(file_1)+"\" \n")
            #calculate curve
            x_calc = np.arange(x_min, x_max, step)
            y_calc = func(x_calc, *p1_opt)
            xy_calc = np.column_stack((x_calc, y_calc))
            #save fit curve
            c=(c+1)
            fit=(str(base_1)+'_FR_OM_PA_fit.data')
            draw.write("read xy \""+str(fit)+"\" \n")
            draw.write("s"+str(c)+" symbol 0 \n")
            draw.write("s"+str(c)+" line type 1 \n")
            draw.write("s"+str(c)+" line color 1 \n")
            draw.write("s"+str(c)+" layer 52 \n")
            draw.write("s"+str(c)+" legend off \n")
            np.savetxt(fit,xy_calc,fmt='%.4e')
            #get color
            i = i + 1
            color = (color_list[i])
            # plot
            plt.plot(x_calc, y_calc, color)
            plt.errorbar(x_data_1, y_data_1, xerr=None, yerr=y_data_err_1, fmt = color + "o")

#partial agonist best fit
#select file
dialog = wx.FileDialog(None, "Choose dat file of partial agonist", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected_2=dialog.GetPath()
    data_2 = np.loadtxt(selected_2)
    columns = np.size((data_2)[0,:])
#test wheter we have data
if columns == 0:
    msg = ('Empty data file\n')
    errors = msg
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
else:
    #initial best fit for depleted system
    path_2, file_2=os.path.split(selected_2)
    base_2=os.path.splitext(selected_2)[0]
    res.write("\npartial agonist\n")
    # load data
    x_data_2 = data_2[:,0]
    y_data_2 = data_2[:,1]
    y_data_err_2 = data_2[:,2]
    x_min = np.amin(x_data_2)
    x_max = np.amax(x_data_2)
    y_min = np.amin(y_data_2)
    y_max = np.amax(y_data_2)
    if np.size(x_data_2) < 5 or (x_max - x_min) < 2.5:
        msg = ('Too few data points in ' +str(file_2)+ ' This data will be skipped\n')
        errors = errors + msg
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    else:
        if x_min < -15 or x_max > 0:
            msg = ('X value out of range ,<15,0>! '+str(file_2)+' will be skipped\n')
            errors = errors + msg
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
            Emax2_estim = Emax1_calc
            Emax2_min = Emax1_calc * 0.8
            Emax2_max = Emax1_calc * 1.2            
            tau2_estim = (y_max - basal) / (Emax1_calc - y_max)
            tau2_min = 0.1 * tau2_estim
            tau2_max = 10 * tau2_estim
            #Get agonist affinity
            ask = ('Enter pKA of agonist for '+str(file_2)+'\n')
            dlg = wx.TextEntryDialog(None, ask, "Input",'-6')
            if dlg.ShowModal() == wx.ID_OK:
                pKA2 = float(dlg.GetValue())
            dlg.Destroy()
            p2 = [tau2_estim, Emax2_estim]
            #fit data
            def func(x, tau2, Emax2):
                return basal + ((10**x) * tau2 * (Emax2 - basal)) / ((10**x) * (1 +tau2) + (10**pKA2))
            p2_opt, p2_cov = opt.curve_fit(func, x_data_2, y_data_2, p2, bounds=([tau2_min, Emax2_min],[tau2_max,Emax2_max]))
            p2_err = np.sqrt(np.diag(p2_cov))
            tau2_calc = (p2_opt[0])
            Emax2_calc = (p2_opt[1])
            tau2_err = (p2_err[0])
            Emax2_err = (p2_err[1])
            #write results
            tau2_res = (str("{0:.4f}".format(tau2_calc))+' ± '+str("{0:.4f}".format(tau2_err)))
            Emax2_res = (str("{0:.2f}".format(Emax2_calc))+' ± '+str("{0:.2f}".format(Emax2_err)))
            res.write(str(tau2_res)+"\t"+str(Emax2_res)+"\t"+str(pKA2)+"\t"+str(file_2)+"\n")
            #write Grace plot
            c=(c+1)
            d=(d+1)
            draw.write("read xydy \""+str(selected_2)+"\" \n")
            draw.write("s"+str(c)+" symbol "+str(d)+" \n")
            draw.write("s"+str(c)+" symbol size 0.8 \n")
            draw.write("s"+str(c)+" symbol color 1 \n")
            draw.write("s"+str(c)+" symbol fill color 0 \n")
            draw.write("s"+str(c)+" symbol fill pattern 1 \n")
            draw.write("s"+str(c)+" errorbar color 1 \n")
            draw.write("s"+str(c)+" errorbar size 0.8 \n")
            draw.write("s"+str(c)+" line type 0 \n")
            draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau2_calc))+' \\#{B1} '+str("{0:.4f}".format(tau2_err))+"; E\\sMAX\\N="+str("{0:.2f}".format(Emax2_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax2_err))+"; pK\\sA\\N="+str("{0:.2f}".format(pKA2))+"; "+str(file_2)+"\" \n")
            #calculate curve
            x_calc = np.arange(x_min, x_max, step)
            y_calc = func(x_calc, *p2_opt)
            xy_calc = np.column_stack((x_calc, y_calc))
            #save fit curve
            c=(c+1)
            fit=(str(base_2)+'_FR_OM_PA_fit.data')
            draw.write("read xy \""+str(fit)+"\" \n")
            draw.write("s"+str(c)+" symbol 0 \n")
            draw.write("s"+str(c)+" line type 1 \n")
            draw.write("s"+str(c)+" line color 1 \n")
            draw.write("s"+str(c)+" layer 52 \n")
            draw.write("s"+str(c)+" legend off \n")
            
            np.savetxt(fit,xy_calc,fmt='%.4e')
            
            #get color
            i = i + 1
            color = (color_list[i])
            # add to plot
            plt.plot(x_calc, y_calc, color)
            plt.errorbar(x_data_2, y_data_2, xerr=None, yerr=y_data_err_2, fmt = color + "o")

#Second partial agonist best fit
#select file
dialog = wx.FileDialog(None, "Choose dat file of second partial agonist", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected_3=dialog.GetPath()
    data_3 = np.loadtxt(selected_3)
    columns = np.size((data_3)[0,:])
#test wheter we have data
if columns == 0:
    msg = ('Empty data file\n')
    errors = msg
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
else:
    #initial best fit for depleted system
    path_3, file_3=os.path.split(selected_3)
    base_3=os.path.splitext(selected_3)[0]
    res.write("\npartial agonist\n")
    # load data
    x_data_3 = data_3[:,0]
    y_data_3 = data_3[:,1]
    y_data_err_3 = data_3[:,2]
    x_min = np.amin(x_data_3)
    x_max = np.amax(x_data_3)
    y_min = np.amin(y_data_3)
    y_max = np.amax(y_data_3)
    if np.size(x_data_3) < 5 or (x_max - x_min) < 2.5:
        msg = ('Too few data points in ' +str(file_3)+ ' This data will be skipped\n')
        errors = errors + msg
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    else:
        if x_min < -15 or x_max > 0:
            msg = ('X value out of range ,<15,0>! '+str(file_3)+' will be skipped\n')
            errors = errors + msg
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
            Emax3_estim = Emax1_calc
            Emax3_min = Emax1_calc * 0.8
            Emax3_max = Emax1_calc * 1.2            
            tau3_estim = (y_max - basal) / (Emax1_calc - y_max)
            tau3_min = 0.1 * tau3_estim
            tau3_max = 10 * tau3_estim
            #Get agonist affinity
            ask = ('Enter pKA of agonist for '+str(file_3)+'\n')
            dlg = wx.TextEntryDialog(None, ask, "Input",'-6')
            if dlg.ShowModal() == wx.ID_OK:
                pKA3 = float(dlg.GetValue())
            dlg.Destroy()
            p3 = [tau3_estim, Emax3_estim]
            #fit data
            def func(x, tau3, Emax3):
                return basal + ((10**x) * tau3 * (Emax3 - basal)) / ((10**x) * (1 +tau3) + (10**pKA3))
            p3_opt, p3_cov = opt.curve_fit(func, x_data_3, y_data_3, p3, bounds=([tau3_min, Emax3_min],[tau3_max, Emax3_max]))
            p3_err = np.sqrt(np.diag(p3_cov))
            tau3_calc = (p3_opt[0])
            Emax3_calc = (p3_opt[1])
            tau3_err = (p3_err[0])
            Emax3_err = (p3_err[1])
            #write results
            tau3_res = (str("{0:.4f}".format(tau3_calc))+' ± '+str("{0:.4f}".format(tau3_err)))
            Emax3_res = (str("{0:.2f}".format(Emax3_calc))+' ± '+str("{0:.2f}".format(Emax3_err)))
            res.write(str(tau3_res)+"\t"+str(Emax3_res)+"\t"+str(pKA3)+"\t"+str(file_3)+"\n")
            #write Grace plot
            c=(c+1)
            d=(d+1)
            draw.write("read xydy \""+str(selected_3)+"\" \n")
            draw.write("s"+str(c)+" symbol "+str(d)+" \n")
            draw.write("s"+str(c)+" symbol size 0.8 \n")
            draw.write("s"+str(c)+" symbol color 1 \n")
            draw.write("s"+str(c)+" symbol fill color 0 \n")
            draw.write("s"+str(c)+" symbol fill pattern 1 \n")
            draw.write("s"+str(c)+" errorbar color 1 \n")
            draw.write("s"+str(c)+" errorbar size 0.8 \n")
            draw.write("s"+str(c)+" line type 0 \n")
            draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau3_calc))+' \\#{B1} '+str("{0:.4f}".format(tau3_err))+"; E\\sMAX\\N="+str("{0:.2f}".format(Emax3_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax3_err))+"; pK\\sA\\N="+str("{0:.2f}".format(pKA3))+"; "+str(file_3)+"\" \n")
            #calculate curve
            x_calc = np.arange(x_min, x_max, step)
            y_calc = func(x_calc, *p3_opt)
            xy_calc = np.column_stack((x_calc, y_calc))
            #save fit curve
            c=(c+1)
            fit=(str(base_3)+'_FR_OM_PA_fit.data')
            draw.write("read xy \""+str(fit)+"\" \n")
            draw.write("s"+str(c)+" symbol 0 \n")
            draw.write("s"+str(c)+" line type 1 \n")
            draw.write("s"+str(c)+" line color 1 \n")
            draw.write("s"+str(c)+" layer 52 \n")
            draw.write("s"+str(c)+" legend off \n")
            
            np.savetxt(fit,xy_calc,fmt='%.4e')
            
            #get color
            i = i + 1
            color = (color_list[i])
            # add to plot
            plt.plot(x_calc, y_calc, color)
            plt.errorbar(x_data_3, y_data_3, xerr=None, yerr=y_data_err_3, fmt = color + "o")

#Third partial agonist best fit
#select file
dialog = wx.FileDialog(None, "Choose dat file of third partial agonist", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected_4=dialog.GetPath()
    data_4 = np.loadtxt(selected_4)
    columns = np.size((data_4)[0,:])
#test wheter we have data
if columns == 0:
    msg = ('Empty data file\n')
    errors = msg
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
else:
    #initial best fit for depleted system
    path_4, file_4=os.path.split(selected_4)
    base_4=os.path.splitext(selected_4)[0]
    res.write("\npartial agonist\n")
    # load data
    x_data_4 = data_4[:,0]
    y_data_4 = data_4[:,1]
    y_data_err_4 = data_4[:,2]
    x_min = np.amin(x_data_4)
    x_max = np.amax(x_data_4)
    y_min = np.amin(y_data_4)
    y_max = np.amax(y_data_4)
    if np.size(x_data_4) < 5 or (x_max - x_min) < 2.5:
        msg = ('Too few data points in ' +str(file_4)+ ' This data will be skipped\n')
        errors = errors + msg
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    else:
        if x_min < -15 or x_max > 0:
            msg = ('X value out of range ,<15,0>! '+str(file_4)+' will be skipped\n')
            errors = errors + msg
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
            Emax4_estim = Emax1_calc
            Emax4_min = Emax1_calc * 0.8
            Emax4_max = Emax1_calc * 1.2            
            tau4_estim = (y_max - basal) / (Emax1_calc - y_max)
            tau4_min = 0.1 * tau4_estim
            tau4_max = 10 * tau4_estim
            #Get agonist affinity
            ask = ('Enter pKA of agonist for '+str(file_4)+'\n')
            dlg = wx.TextEntryDialog(None, ask, "Input",'-6')
            if dlg.ShowModal() == wx.ID_OK:
                pKA4 = float(dlg.GetValue())
            dlg.Destroy()
            p4 = [tau4_estim, Emax4_estim]
            #fit data
            def func(x, tau4, Emax4):
                return basal + ((10**x) * tau4 * (Emax4 - basal)) / ((10**x) * (1 +tau4) + (10**pKA4))
            p4_opt, p4_cov = opt.curve_fit(func, x_data_4, y_data_4, p4, bounds=([tau4_min, Emax4_min],[tau4_max, Emax4_max]))
            p4_err = np.sqrt(np.diag(p4_cov))
            tau4_calc = (p4_opt[0])
            Emax4_calc = (p4_opt[1])
            tau4_err = (p4_err[0])
            Emax4_err = (p4_err[1])
            #write results
            tau4_res = (str("{0:.4f}".format(tau4_calc))+' ± '+str("{0:.4f}".format(tau4_err)))
            Emax4_res = (str("{0:.2f}".format(Emax4_calc))+' ± '+str("{0:.2f}".format(Emax4_err)))
            res.write(str(tau4_res)+"\t"+str(Emax4_res)+"\t"+str(pKA4)+"\t"+str(file_4)+"\n")
            #write Grace plot
            c=(c+1)
            d=(d+1)
            draw.write("read xydy \""+str(selected_4)+"\" \n")
            draw.write("s"+str(c)+" symbol "+str(d)+" \n")
            draw.write("s"+str(c)+" symbol size 0.8 \n")
            draw.write("s"+str(c)+" symbol color 1 \n")
            draw.write("s"+str(c)+" symbol fill color 0 \n")
            draw.write("s"+str(c)+" symbol fill pattern 1 \n")
            draw.write("s"+str(c)+" errorbar color 1 \n")
            draw.write("s"+str(c)+" errorbar size 0.8 \n")
            draw.write("s"+str(c)+" line type 0 \n")
            draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau4_calc))+' \\#{B1} '+str("{0:.4f}".format(tau4_err))+"; E\\sMAX\\N="+str("{0:.2f}".format(Emax4_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax4_err))+"; pK\\sA\\N="+str("{0:.2f}".format(pKA4))+"; "+str(file_4)+"\" \n")
            #calculate curve
            x_calc = np.arange(x_min, x_max, step)
            y_calc = func(x_calc, *p4_opt)
            xy_calc = np.column_stack((x_calc, y_calc))
            #save fit curve
            c=(c+1)
            fit=(str(base_4)+'_FR_OM_PA_fit.data')
            draw.write("read xy \""+str(fit)+"\" \n")
            draw.write("s"+str(c)+" symbol 0 \n")
            draw.write("s"+str(c)+" line type 1 \n")
            draw.write("s"+str(c)+" line color 1 \n")
            draw.write("s"+str(c)+" layer 52 \n")
            draw.write("s"+str(c)+" legend off \n")
            
            np.savetxt(fit,xy_calc,fmt='%.4e')
            
            #get color
            i = i + 1
            color = (color_list[i])
            # add to plot
            plt.plot(x_calc, y_calc, color)
            plt.errorbar(x_data_4, y_data_4, xerr=None, yerr=y_data_err_4, fmt = color + "o")
    
#Global fit
if np.any(x_data_1 != x_data_2) or np.any(x_data_1 != x_data_3) or np.any(x_data_1 != x_data_4):
    msg = ('X-data differ between sets.\nGlobal fit will not be performed\n')
    errors = errors + msg
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
else:
    res.write("\nGlobal fit with shared Emax\n")
    #fit data
    def func(x, p):
        tau, Emax, pKA = p
        return basal + ((10**x) * tau * (Emax - basal)) / ((10**x) * (1 +tau) + (10**pKA))
    def err(p, x, y):
        return func(x, p) - y
    def err_global(p, x, y1, y2, y3, y4):
        # p is now a_1, b, c_1, a_2, c_2, with b shared between the two
        p_1 = p[0], p[1], pKA1
        p_2 = p[2], p[1], pKA2
        p_3 = p[3], p[1], pKA3
        p_4 = p[4], p[1], pKA4
        err1 = err(p_1, x, y1)
        err2 = err(p_2, x, y2)
        err3 = err(p_3, x, y3)
        err4 = err(p_4, x, y4)
        return np.concatenate((err1, err2, err3, err4))
    pg_estim = [p1_opt[0], p1_opt[1], p2_opt[0], p3_opt[0], p4_opt[0]]
    pg_opt, cov_x, infodict, errmsg, success = opt.leastsq(err_global, pg_estim, args=(x_data_1, y_data_1, y_data_2, y_data_3, y_data_4), full_output=1, epsfcn=0.0001)
    residuals = err_global(pg_opt, x_data_1, y_data_1, y_data_2, y_data_3, y_data_4)
    reduced_chi_square = np.sum(residuals**2)/(len(x_data_1)-2)
    pg_cov = cov_x * reduced_chi_square
    pg_err = np.sqrt(np.diag(pg_cov))
    pg1_opt = [pg_opt[0], pg_opt[1], pKA1]
    pg2_opt = [pg_opt[2], pg_opt[1], pKA2]
    pg3_opt = [pg_opt[3], pg_opt[1], pKA3]
    pg4_opt = [pg_opt[4], pg_opt[1], pKA4]
    tau1_calc = (pg_opt[0])
    tau1_err = (pg_err[0])
    Emax1_calc = (pg_opt[1])
    Emax1_err = (pg_err[1])
    tau2_calc = (pg_opt[2])
    tau2_err = (pg_err[2])
    Emax2_calc = (pg_opt[1])
    Emax2_err = (pg_err[1])
    tau3_calc = (pg_opt[3])
    tau3_err = (pg_err[3])
    Emax3_calc = (pg_opt[1])
    Emax3_err = (pg_err[1])
    tau4_calc = (pg_opt[4])
    tau4_err = (pg_err[4])
    Emax4_calc = (pg_opt[1])
    Emax4_err = (pg_err[1])
    #write results
    tau1_res = (str("{0:.4f}".format(tau1_calc))+' ± '+str("{0:.4f}".format(tau1_err)))
    Emax1_res = (str("{0:.2f}".format(Emax1_calc))+' ± '+str("{0:.2f}".format(Emax1_err)))
    res.write(str(tau1_res)+"\t"+str(Emax1_res)+"\t"+str(pKA1)+"\t"+str(file_1)+"\n")
    tau2_res = (str("{0:.4f}".format(tau2_calc))+' ± '+str("{0:.4f}".format(tau2_err)))
    Emax2_res = (str("{0:.2f}".format(Emax2_calc))+' ± '+str("{0:.2f}".format(Emax2_err)))
    res.write(str(tau2_res)+"\t"+str(Emax2_res)+"\t"+str(pKA2)+"\t"+str(file_2)+"\n")
    tau3_res = (str("{0:.4f}".format(tau3_calc))+' ± '+str("{0:.4f}".format(tau3_err)))
    Emax3_res = (str("{0:.2f}".format(Emax3_calc))+' ± '+str("{0:.2f}".format(Emax3_err)))
    res.write(str(tau3_res)+"\t"+str(Emax3_res)+"\t"+str(pKA3)+"\t"+str(file_3)+"\n")
    tau4_res = (str("{0:.4f}".format(tau4_calc))+' ± '+str("{0:.4f}".format(tau4_err)))
    Emax4_res = (str("{0:.2f}".format(Emax4_calc))+' ± '+str("{0:.2f}".format(Emax4_err)))
    res.write(str(tau4_res)+"\t"+str(Emax4_res)+"\t"+str(pKA4)+"\t"+str(file_4)+"\n")
    #calculate curve 1
    x_calc = np.arange(x_min, x_max, step)
    y_calc = func(x_calc, pg1_opt)
    xy_calc = np.column_stack((x_calc, y_calc))
    #write Grace plot curve 1
    c=(c+1)
    fit=(str(base_1)+'_FR_OM_PA_gfit.data')
    draw.write("read xy \""+str(fit)+"\" \n")
    draw.write("s"+str(c)+" symbol 0 \n")
    draw.write("s"+str(c)+" line type 1 \n")
    draw.write("s"+str(c)+" line linestyle 2 \n")
    draw.write("s"+str(c)+" line linewidth 2 \n")
    draw.write("s"+str(c)+" line color 2 \n")
    draw.write("s"+str(c)+" layer 51 \n")
    draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau1_calc))+' \\#{B1} '+str("{0:.4f}".format(tau1_err))+"; E\\sMAX\\N="+str("{0:.2f}".format(Emax1_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax1_err))+"; pK\\sA\\N="+str("{0:.2f}".format(pKA1))+"; "+str(file_1)+"\" \n")
    
    np.savetxt(fit,xy_calc,fmt='%.4e')
    
    # add to plot
    plt.plot(x_calc, y_calc, 'y', linestyle='--')
    #calculate curve 2
    x_calc = np.arange(x_min, x_max, step)
    y_calc = func(x_calc, pg2_opt)
    xy_calc = np.column_stack((x_calc, y_calc))
    #write Grace plot curve 2
    c=(c+1)
    fit=(str(base_2)+'_FR_OM_PA_gfit.data')
    draw.write("read xy \""+str(fit)+"\" \n")
    draw.write("s"+str(c)+" symbol 0 \n")
    draw.write("s"+str(c)+" line type 1 \n")
    draw.write("s"+str(c)+" line linestyle 2 \n")
    draw.write("s"+str(c)+" line linewidth 2 \n")
    draw.write("s"+str(c)+" line color 2 \n")
    draw.write("s"+str(c)+" layer 51 \n")
    draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau2_calc))+' \\#{B1} '+str("{0:.4f}".format(tau2_err))+"; E\\sMAX\\N="+str("{0:.2f}".format(Emax2_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax2_err))+"; pK\\sA\\N="+str("{0:.2f}".format(pKA2))+"; "+str(file_2)+"\" \n")
    
    np.savetxt(fit,xy_calc,fmt='%.4e')
    
    # add to plot
    plt.plot(x_calc, y_calc, 'y', linestyle='--')
    #calculate curve 3
    x_calc = np.arange(x_min, x_max, step)
    y_calc = func(x_calc, pg3_opt)
    xy_calc = np.column_stack((x_calc, y_calc))
    #write Grace plot curve 3
    c=(c+1)
    fit=(str(base_3)+'_FR_OM_PA_gfit.data')
    draw.write("read xy \""+str(fit)+"\" \n")
    draw.write("s"+str(c)+" symbol 0 \n")
    draw.write("s"+str(c)+" line type 1 \n")
    draw.write("s"+str(c)+" line linestyle 2 \n")
    draw.write("s"+str(c)+" line linewidth 2 \n")
    draw.write("s"+str(c)+" line color 2 \n")
    draw.write("s"+str(c)+" layer 51 \n")
    draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau3_calc))+' \\#{B1} '+str("{0:.4f}".format(tau3_err))+"; E\\sMAX\\N="+str("{0:.2f}".format(Emax3_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax3_err))+"; pK\\sA\\N="+str("{0:.2f}".format(pKA3))+"; "+str(file_3)+"\" \n")
    
    np.savetxt(fit,xy_calc,fmt='%.4e')
    
    # add to plot
    plt.plot(x_calc, y_calc, 'y', linestyle='--')
    #calculate curve 4
    x_calc = np.arange(x_min, x_max, step)
    y_calc = func(x_calc, pg4_opt)
    xy_calc = np.column_stack((x_calc, y_calc))
    #write Grace plot curve 4
    c=(c+1)
    fit=(str(base_4)+'_FR_OM_PA_gfit.data')
    draw.write("read xy \""+str(fit)+"\" \n")
    draw.write("s"+str(c)+" symbol 0 \n")
    draw.write("s"+str(c)+" line type 1 \n")
    draw.write("s"+str(c)+" line linestyle 2 \n")
    draw.write("s"+str(c)+" line linewidth 2 \n")
    draw.write("s"+str(c)+" line color 2 \n")
    draw.write("s"+str(c)+" layer 51 \n")
    draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau4_calc))+' \\#{B1} '+str("{0:.4f}".format(tau4_err))+"; E\\sMAX\\N="+str("{0:.2f}".format(Emax4_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax4_err))+"; pK\\sA\\N="+str("{0:.2f}".format(pKA4))+"; "+str(file_4)+"\" \n")
    
    np.savetxt(fit,xy_calc,fmt='%.4e')
    
    # add to plot
    plt.plot(x_calc, y_calc, 'y', linestyle='--')

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
log.write(errors)
log.close()
