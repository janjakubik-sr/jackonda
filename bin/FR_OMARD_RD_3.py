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
    basal = dlg.GetValue()
    basal =  float(basal)
dlg.Destroy()

#Get Emax estimate
ask = ('Enter your estimate of system Emax')
dlg = wx.TextEntryDialog(None, ask, "Input",'1')
if dlg.ShowModal() == wx.ID_OK:
    global Emax_estim
    Emax_estim = dlg.GetValue()
    Emax_estim =  float(Emax_estim)
dlg.Destroy()
Emax_min = Emax_estim * 0.1
Emax_max = Emax_estim * 10

#Get logKA estimate
ask = ('Enter your estimate of logKA')
dlg = wx.TextEntryDialog(None, ask, "Input",'-6')
if dlg.ShowModal() == wx.ID_OK:
    global logKA_estim
    logKA_estim = dlg.GetValue()
    logKA_estim =  float(logKA_estim)
dlg.Destroy()
logKA_min = logKA_estim - 1
logKA_max = logKA_estim + 1

#Get alpha estimate
ask = ('Enter your estimate of binding cooperativity alpha')
dlg = wx.TextEntryDialog(None, ask, "Input",'0.1')
if dlg.ShowModal() == wx.ID_OK:
    global alpha_estim
    alpha_estim = dlg.GetValue()
    alpha_estim =  float(alpha_estim)
dlg.Destroy()
alpha_min = alpha_estim * 0.1
alpha_max = alpha_estim * 10

#Get beta estimate
ask = ('Enter your estimate of operational cooperativity')
dlg = wx.TextEntryDialog(None, ask, "Input",'0.3')
if dlg.ShowModal() == wx.ID_OK:
    global beta_estim
    beta_estim = dlg.GetValue()
    beta_estim =  float(beta_estim)
dlg.Destroy()
beta_min = beta_estim * 0.1
beta_max = beta_estim * 10

#FR function
def func(x, tau, Emax, logKA, alpha, beta):
    return ( Emax*(beta*tau*(10**x)*(2*(10**logKA)+alpha*(10**x))**2)/(beta*tau*(10**x)*(2*(10**logKA)+alpha*(10**x))**2+(2*beta*(10**logKA)+alpha*(10**x))*((10**logKA)**2+2*(10**x)*(10**logKA)+alpha*(10**x)**2)) )

#Native system best fit
#select file
dialog = wx.FileDialog(None, "Choose dat file of HIGH recepor system", os.getcwd(), "","*.dat", wx.FD_OPEN)
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
    set_1=os.path.basename(selected_1).split('/')[-1]
    if os.path.isfile("FR_OMARD_RD.res"):
        os.remove("FR_OMARD_RD.res")
    res = open("FR_OMARD_RD.res","w")
    res.write("Functional response - OMARD - Receptor depletion\n\n")
    res.write("tau\t\tEmax\t\tpKA\t\talpha\t\tbeta\t\tData file\n")
    #prepare file for Grace plot
    if os.path.isfile("FR_OMARD_RD.draw"):
        os.remove("FR_OMARD_RD.draw")
    draw = open("FR_OMARD_RD.draw","w")
    c=-1 #plot counter
    d=0  #symbolcounter
    #initial best fit for full agonist
    i = -1
    res.write("\nHigh receptor system\n")
    # load data
    x_data_1 = data_1[:,0]
    y_data_1 = data_1[:,1]
    y_data_err_1 = data_1[:,2]
    x_min_1 = np.amin(x_data_1)
    x_max_1 = np.amax(x_data_1)
    y_min_1 = np.amin(y_data_1)
    y_max_1 = np.amax(y_data_1)
    if np.size(x_data_1) < 7 or (x_max_1 - x_min_1) < 4:
        msg = ('Too few data points in ' +str(file_1)+ ' This data will be skipped\n')
        errors = errors + msg
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    else:
        if x_min_1 < -15 or x_max_1 > 0:
            msg = ('X value out of range ,<15,0>! '+str(file_1)+' will be skipped\n')
            errors = errors + msg
            dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            if x_max_1 > x_max_max:
                x_max_max = x_max_1
            if x_min_1 < x_min_min:
                x_min_min = x_min_1
            if y_max_1 > y_max_max:
                y_max_max = y_max_1
            #calculate estimates
            tau1_estim = (y_max_1 - basal) / (Emax_estim - y_max_1)
            tau1_min = tau1_estim * 0.1
            tau1_max = tau1_estim * 10
            p1 = [tau1_estim, Emax_estim, logKA_estim, alpha_estim, beta_estim]
            #fit data
            p1_opt, p1_cov = opt.curve_fit(func, x_data_1, y_data_1, p1, bounds=([tau1_min, Emax_min, logKA_min, alpha_min, beta_min],[tau1_max, Emax_max, logKA_max, alpha_max, beta_max]))
            p1_err = np.sqrt(np.diag(p1_cov))
            tau1_calc = (p1_opt[0])
            Emax1_calc = (p1_opt[1])
            logKA1_calc = (p1_opt[2])
            alpha1_calc = (p1_opt[3])
            beta1_calc = (p1_opt[4])
            tau1_err = (p1_err[0])
            Emax1_err = (p1_err[1])
            logKA1_err = (p1_err[2])
            alpha1_err = (p1_err[3])
            beta1_err = (p1_err[4])
            #write results
            tau1_res = (str("{0:.4f}".format(tau1_calc))+' ± '+str("{0:.4f}".format(tau1_err)))
            Emax1_res = (str("{0:.2f}".format(Emax1_calc))+' ± '+str("{0:.2f}".format(Emax1_err)))
            logKA1_res = (str("{0:.2f}".format(logKA1_calc))+' ± '+str("{0:.2f}".format(logKA1_err)))
            alpha1_res = (str("{0:.2f}".format(alpha1_calc))+' ± '+str("{0:.2f}".format(alpha1_err)))
            beta1_res = (str("{0:.2f}".format(beta1_calc))+' ± '+str("{0:.2f}".format(beta1_err)))
            res.write(str(tau1_res)+"\t"+str(Emax1_res)+"\t"+str(logKA1_res)+"\t"+str(set_1)+"\n")
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
            draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau1_calc))+' \\#{B1} '+str("{0:.4f}".format(tau1_err))+"; E\\sMAX\\N="+str("{0:.2f}".format(Emax1_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax1_err))+"; pK\\sA\\N="+str("{0:.2f}".format(logKA1_calc))+' \\#{B1} '+str("{0:.2f}".format(logKA1_err))+"; \\f{Symbol}a\\f{}="+str("{0:.4f}".format(alpha1_calc))+' \\#{B1} '+str("{0:.4f}".format(alpha1_err))+"; \\f{Symbol}b\\f{}="+str("{0:.4f}".format(beta1_calc))+' \\#{B1} '+str("{0:.4f}".format(beta1_err))+"; "+str(set_1)+"\" \n")
            #calculate curve
            fit=(str(base_1)+'_FR_OMARD_RD_fit.data')
            x_calc = np.linspace((x_min_1),(x_max_1), 121)
            y_calc = func(x_calc, *p1_opt)
            xy_calc = np.column_stack((x_calc, y_calc))
            np.savetxt(fit,xy_calc,fmt='%.4e')
            #get color
            i = i + 1
            color = (color_list[i])
            # plot
            plt.plot(x_calc, y_calc, color)
            plt.errorbar(x_data_1, y_data_1, xerr=None, yerr=y_data_err_1, fmt = color + "o")
            #add curve to Grace plot
            c=(c+1)
            draw.write("read xy \""+str(fit)+"\" \n")
            draw.write("s"+str(c)+" symbol 0 \n")
            draw.write("s"+str(c)+" line type 1 \n")
            draw.write("s"+str(c)+" line color 1 \n")
            draw.write("s"+str(c)+" layer 52 \n")
            draw.write("s"+str(c)+" legend off \n")

#Delpeted system best fit
#select file
dialog = wx.FileDialog(None, "Choose dat file of LOW receptor system", os.getcwd(), "","*.dat", wx.FD_OPEN)
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
    set_2=os.path.basename(selected_2).split('/')[-1]
    res.write("\nLow receptor system\n")
    # load data
    x_data_2 = data_2[:,0]
    y_data_2 = data_2[:,1]
    y_data_err_2 = data_2[:,2]
    x_min_2 = np.amin(x_data_2)
    x_max_2 = np.amax(x_data_2)
    y_min_2 = np.amin(y_data_2)
    y_max_2 = np.amax(y_data_2)
    if np.size(x_data_2) < 5 or (x_max_2 - x_min_2) < 2.5:
        msg = ('Too few data points in ' +str(file_2)+ ' This data will be skipped\n')
        errors = errors + msg
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    else:
        if x_min_2 < -15 or x_max_2 > 0:
            msg = ('X value out of range ,<15,0>! '+str(file_2)+' will be skipped\n')
            errors = errors + msg
            dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            if x_max_2 > x_max_max:
                x_max_max = x_max_2
            if x_min_2 < x_min_min:
                x_min_min = x_min_2
            if y_max_2 > y_max_max:
                y_max_max = y_max_2
            #calculate estimates
            tau2_estim = (y_max_2 - basal) / (Emax_estim - y_max_2)
            tau2_min = tau2_estim * 0.1
            tau2_max = tau2_estim * 10
            p2 = [tau2_estim, Emax_estim, logKA_estim, alpha_estim, beta_estim]
            #fit data
            p2_opt, p2_cov = opt.curve_fit(func, x_data_2, y_data_2, p2, bounds=([tau2_min, Emax_min, logKA_min, alpha_min, beta_min],[tau2_max, Emax_max, logKA_max, alpha_max, beta_max]))
            p2_err = np.sqrt(np.diag(p2_cov))
            tau2_calc = (p2_opt[0])
            Emax2_calc = (p2_opt[1])
            logKA2_calc = (p2_opt[2])
            alpha2_calc = (p2_opt[3])
            beta2_calc = (p2_opt[4])
            tau2_err = (p2_err[0])
            Emax2_err = (p2_err[1])
            logKA2_err = (p2_err[2])
            alpha2_err = (p2_err[3])
            beta2_err = (p2_err[4])
            #write results
            tau2_res = (str("{0:.4f}".format(tau2_calc))+' ± '+str("{0:.4f}".format(tau2_err)))
            Emax2_res = (str("{0:.2f}".format(Emax2_calc))+' ± '+str("{0:.2f}".format(Emax2_err)))
            logKA2_res = (str("{0:.2f}".format(logKA2_calc))+' ± '+str("{0:.2f}".format(logKA2_err)))
            alpha2_res = (str("{0:.2f}".format(alpha2_calc))+' ± '+str("{0:.2f}".format(alpha2_err)))
            beta2_res = (str("{0:.2f}".format(beta2_calc))+' ± '+str("{0:.2f}".format(beta2_err)))
            res.write(str(tau2_res)+"\t"+str(Emax2_res)+"\t"+str(logKA2_res)+"\t"+str(set_2)+"\n")
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
            draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau2_calc))+' \\#{B1} '+str("{0:.4f}".format(tau2_err))+"; E\\sMAX\\N="+str("{0:.2f}".format(Emax2_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax2_err))+"; pK\\sA\\N="+str("{0:.2f}".format(logKA2_calc))+' \\#{B1} '+str("{0:.2f}".format(logKA2_err))+"; \\f{Symbol}a\\f{}="+str("{0:.4f}".format(alpha2_calc))+' \\#{B1} '+str("{0:.4f}".format(alpha2_err))+"; \\f{Symbol}b\\f{}="+str("{0:.4f}".format(beta2_calc))+' \\#{B1} '+str("{0:.4f}".format(beta2_err))+"; "+str(set_2)+"\" \n")
            #calculate curve
            fit=(str(base_2)+'_FR_OMARD_RD_fit.data')
            x_calc = np.linspace((x_min_2),(x_max_2), 121)
            y_calc = func(x_calc, *p2_opt)
            xy_calc = np.column_stack((x_calc, y_calc))
            np.savetxt(fit,xy_calc,fmt='%.4e')
            #get color
            i = i + 1
            color = (color_list[i])
            # add to plot
            plt.plot(x_calc, y_calc, color)
            plt.errorbar(x_data_2, y_data_2, xerr=None, yerr=y_data_err_2, fmt = color + "o")
            #add curve to Grace plot
            c=(c+1)
            draw.write("read xy \""+str(fit)+"\" \n")
            draw.write("s"+str(c)+" symbol 0 \n")
            draw.write("s"+str(c)+" line type 1 \n")
            draw.write("s"+str(c)+" line color 1 \n")
            draw.write("s"+str(c)+" layer 52 \n")
            draw.write("s"+str(c)+" legend off \n")

#Second delpeted system best fit
#select file
dialog = wx.FileDialog(None, "Choose dat file of second LOW receptor system", os.getcwd(), "","*.dat", wx.FD_OPEN)
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
    set_3=os.path.basename(selected_3).split('/')[-1]
    res.write("\nLow receptor system\n")
    # load data
    x_data_3 = data_3[:,0]
    y_data_3 = data_3[:,1]
    y_data_err_3 = data_3[:,2]
    x_min_3 = np.amin(x_data_3)
    x_max_3 = np.amax(x_data_3)
    y_min_3 = np.amin(y_data_3)
    y_max_3 = np.amax(y_data_3)
    if np.size(x_data_3) < 5 or (x_max_3 - x_min_3) < 2.5:
        msg = ('Too few data points in ' +str(file_3)+ ' This data will be skipped\n')
        errors = errors + msg
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    else:
        if x_min_3 < -15 or x_max_3 > 0:
            msg = ('X value out of range ,<15,0>! '+str(file_3)+' will be skipped\n')
            errors = errors + msg
            dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            if x_max_3 > x_max_max:
                x_max_max = x_max_3
            if x_min_3 < x_min_min:
                x_min_min = x_min_3
            if y_max_3 > y_max_max:
                y_max_max = y_max_3
            #calculate estimates
            tau3_estim = (y_max_3 - basal) / (Emax_estim - y_max_3)
            tau3_min = tau3_estim * 0.1
            tau3_max = tau3_estim * 10
            p3 = [tau3_estim, Emax_estim, logKA_estim, alpha_estim, beta_estim]
            #fit data
            p3_opt, p3_cov = opt.curve_fit(func, x_data_3, y_data_3, p3, bounds=([tau3_min, Emax_min, logKA_min, alpha_min, beta_min],[tau3_max, Emax_max, logKA_max, alpha_max, beta_max]))
            p3_err = np.sqrt(np.diag(p3_cov))
            tau3_calc = (p3_opt[0])
            Emax3_calc = (p3_opt[1])
            logKA3_calc = (p3_opt[2])
            alpha3_calc = (p3_opt[3])
            beta3_calc = (p3_opt[4])
            tau3_err = (p3_err[0])
            Emax3_err = (p3_err[1])
            logKA3_err = (p3_err[2])
            alpha3_err = (p3_err[3])
            beta3_err = (p3_err[4])
            #write results
            tau3_res = (str("{0:.4f}".format(tau3_calc))+' ± '+str("{0:.4f}".format(tau3_err)))
            Emax3_res = (str("{0:.2f}".format(Emax3_calc))+' ± '+str("{0:.2f}".format(Emax3_err)))
            logKA3_res = (str("{0:.2f}".format(logKA3_calc))+' ± '+str("{0:.2f}".format(logKA3_err)))
            alpha3_res = (str("{0:.2f}".format(alpha3_calc))+' ± '+str("{0:.2f}".format(alpha3_err)))
            beta3_res = (str("{0:.2f}".format(beta3_calc))+' ± '+str("{0:.2f}".format(beta3_err)))
            res.write(str(tau3_res)+"\t"+str(Emax3_res)+"\t"+str(logKA3_res)+"\t"+str(set_3)+"\n")
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
            draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau3_calc))+' \\#{B1} '+str("{0:.4f}".format(tau3_err))+"; E\\sMAX\\N="+str("{0:.2f}".format(Emax3_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax3_err))+"; pK\\sA\\N="+str("{0:.2f}".format(logKA3_calc))+' \\#{B1} '+str("{0:.2f}".format(logKA3_err))+"; \\f{Symbol}a\\f{}="+str("{0:.4f}".format(alpha3_calc))+' \\#{B1} '+str("{0:.4f}".format(alpha3_err))+"; \\f{Symbol}b\\f{}="+str("{0:.4f}".format(beta3_calc))+' \\#{B1} '+str("{0:.4f}".format(beta3_err))+"; "+str(set_3)+"\" \n")
            #calculate curve
            fit=(str(base_3)+'_FR_OMARD_RD_fit.data')
            x_calc = np.linspace((x_min_3),(x_max_3), 121)
            y_calc = func(x_calc, *p3_opt)
            xy_calc = np.column_stack((x_calc, y_calc))
            np.savetxt(fit,xy_calc,fmt='%.4e')
            #get color
            i = i + 1
            color = (color_list[i])
            # add to plot
            plt.plot(x_calc, y_calc, color)
            plt.errorbar(x_data_3, y_data_3, xerr=None, yerr=y_data_err_3, fmt = color + "o")
            #add curve to Grace plot
            c=(c+1)
            draw.write("read xy \""+str(fit)+"\" \n")
            draw.write("s"+str(c)+" symbol 0 \n")
            draw.write("s"+str(c)+" line type 1 \n")
            draw.write("s"+str(c)+" line color 1 \n")
            draw.write("s"+str(c)+" layer 52 \n")
            draw.write("s"+str(c)+" legend off \n")

#Global fit
if np.any(x_data_1 != x_data_2) or np.any(x_data_1 != x_data_3):
    msg = ('X-data vary among sets.\nGlobal fit will not be performed\n')
    errors = errors + msg
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
else:
    res.write("\nGlobal fit with shared Emax, KA, alpha and beta\n")
    res.write("tau\t\tEmax\t\tpKA\t\talpha\t\tbeta\t\tData file\n")
    #fit data
    def func2_glob(x, p):
        tau, Emax, logKA, alpha, beta = p
        return ( Emax*(beta*tau*(10**x)*(2*(10**logKA)+alpha*(10**x))**2)/(beta*tau*(10**x)*(2*(10**logKA)+alpha*(10**x))**2+(2*beta*(10**logKA)+alpha*(10**x))*((10**logKA)**2+2*(10**x)*(10**logKA)+alpha*(10**x)**2)) )
    def err_2(p, x, y):
        return func2_glob(x, p) - y
    def err2_global(p, x, y1, y2, y3):
        p_21 = p[0], p[1], p[2], p[3], p[4]
        p_22 = p[5], p[1], p[2], p[3], p[4]
        p_23 = p[6], p[1], p[2], p[3], p[4]
        err_21 = err_2(p_21, x, y1)
        err_22 = err_2(p_22, x, y2)
        err_23 = err_2(p_23, x, y3)
        return np.concatenate((err_21, err_22, err_23))
    pg_estim = [p1_opt[0], Emax_estim, logKA_estim, alpha_estim, beta_estim, p2_opt[0], p3_opt[0]]
    pg_opt, cov_x, infodict, errmsg, success = opt.leastsq(err2_global, pg_estim, args=(x_data_1, y_data_1, y_data_2, y_data_3), full_output=1, epsfcn=0.0001)
    residuals = err2_global(pg_opt, x_data_1, y_data_1, y_data_2, y_data_3)
    reduced_chi_square = np.sum(residuals**2)/(len(x_data_1)-3)
    pg_cov = cov_x * reduced_chi_square
    pg_err = np.sqrt(np.diag(pg_cov))
    pg1_opt = [pg_opt[0], pg_opt[1],pg_opt[2],pg_opt[3],pg_opt[4]]
    pg2_opt = [pg_opt[5], pg_opt[1],pg_opt[2],pg_opt[3],pg_opt[4]]
    pg3_opt = [pg_opt[6], pg_opt[1],pg_opt[2],pg_opt[3],pg_opt[4]]
    tau1_calc = (pg_opt[0])
    tau1_err = (pg_err[0])
    Emax_calc = (pg_opt[1])
    Emax_err = (pg_err[1])
    pKA_calc = (pg_opt[2])
    pKA_err = (pg_err[2])
    alpha_calc = (pg_opt[3])
    alpha_err = (pg_err[3])
    beta_calc = (pg_opt[4])
    beta_err = (pg_err[4])
    tau2_calc = (pg_opt[5])
    tau2_err = (pg_err[5])
    tau3_calc = (pg_opt[6])
    tau3_err = (pg_err[6])
#write results
    tau1_res = (str("{0:.4f}".format(tau1_calc))+' ± '+str("{0:.4f}".format(tau1_err)))
    Emax_res = (str("{0:.2f}".format(Emax_calc))+' ± '+str("{0:.2f}".format(Emax_err)))
    pKA_res = (str("{0:.2f}".format(pKA_calc))+' ± '+str("{0:.2f}".format(pKA_err)))
    alpha_res = (str("{0:.4f}".format(alpha_calc))+' ± '+str("{0:.4f}".format(alpha_err)))
    beta_res = (str("{0:.4f}".format(beta_calc))+' ± '+str("{0:.4f}".format(beta_err)))
    res.write(str(tau1_res)+"\t"+str(Emax_res)+"\t"+str(pKA_res)+"\t"+str(alpha_res)+"\t"+str(beta_res)+"\t"+str(set_1)+"\n")
    tau2_res = (str("{0:.4f}".format(tau2_calc))+' ± '+str("{0:.4f}".format(tau2_err)))
    res.write(str(tau2_res)+"\t"+str(Emax_res)+"\t"+str(pKA_res)+"\t"+str(alpha_res)+"\t"+str(beta_res)+"\t"+str(set_2)+"\n")
    tau3_res = (str("{0:.4f}".format(tau3_calc))+' ± '+str("{0:.4f}".format(tau3_err)))
    res.write(str(tau3_res)+"\t"+str(Emax_res)+"\t"+str(pKA_res)+"\t"+str(alpha_res)+"\t"+str(beta_res)+"\t"+str(set_3)+"\n")

    #calculate curve 1
    fit=(str(base_1)+'_FR_OMARD_RD_gfit.data')
    x_calc = np.linspace((x_min_1),(x_max_1), 121)
    y_calc = func2_glob(x_calc, pg1_opt)
    xy_calc = np.column_stack((x_calc, y_calc))
    np.savetxt(fit,xy_calc,fmt='%.4e')
    # add to plot
    plt.plot(x_calc, y_calc, 'y', linestyle='--')
    #write Grace plot curve 1
    c=(c+1)
    draw.write("read xy \""+str(fit)+"\" \n")
    draw.write("s"+str(c)+" symbol 0 \n")
    draw.write("s"+str(c)+" line type 1 \n")
    draw.write("s"+str(c)+" line linestyle 2 \n")
    draw.write("s"+str(c)+" line linewidth 2 \n")
    draw.write("s"+str(c)+" line color 2 \n")
    draw.write("s"+str(c)+" layer 51 \n")
    draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau1_calc))+' \\#{B1} '+str("{0:.4f}".format(tau1_err))+str(set_1)+"\" \n")

    #calculate curve 2
    fit=(str(base_2)+'_FR_OMARD_RD_gfit.data')
    x_calc = np.linspace((x_min_2),(x_max_2), 121)
    y_calc = func2_glob(x_calc, pg2_opt)
    xy_calc = np.column_stack((x_calc, y_calc))
    np.savetxt(fit,xy_calc,fmt='%.4e')
    # add to plot
    plt.plot(x_calc, y_calc, 'y', linestyle='--')
    #write Grace plot curve 2
    c=(c+1)
    draw.write("read xy \""+str(fit)+"\" \n")
    draw.write("s"+str(c)+" symbol 0 \n")
    draw.write("s"+str(c)+" line type 1 \n")
    draw.write("s"+str(c)+" line linestyle 2 \n")
    draw.write("s"+str(c)+" line linewidth 2 \n")
    draw.write("s"+str(c)+" line color 2 \n")
    draw.write("s"+str(c)+" layer 51 \n")
    draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau2_calc))+' \\#{B1} '+str("{0:.4f}".format(tau2_err))+str(set_2)+"\" \n")

    #calculate curve 3
    fit=(str(base_3)+'_FR_OMARD_RD_gfit.data')
    x_calc = np.linspace((x_min_3),(x_max_3), 121)
    y_calc = func2_glob(x_calc, pg3_opt)
    xy_calc = np.column_stack((x_calc, y_calc))
    np.savetxt(fit,xy_calc,fmt='%.4e')
    # add to plot
    plt.plot(x_calc, y_calc, 'y', linestyle='--')
    #write Grace plot curve 3
    c=(c+1)
    draw.write("read xy \""+str(fit)+"\" \n")
    draw.write("s"+str(c)+" symbol 0 \n")
    draw.write("s"+str(c)+" line type 1 \n")
    draw.write("s"+str(c)+" line linestyle 2 \n")
    draw.write("s"+str(c)+" line linewidth 2 \n")
    draw.write("s"+str(c)+" line color 2 \n")
    draw.write("s"+str(c)+" layer 51 \n")
    draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau3_calc))+' \\#{B1} '+str("{0:.4f}".format(tau3_err))+str(set_3)+"\" \n")

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
