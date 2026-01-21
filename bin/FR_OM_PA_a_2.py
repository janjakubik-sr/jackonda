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

#Functional-response function
def func(x, tau, Emax, pKA):
    return 1 + ((10**x) * tau * Emax) / ((10**x) * (1 +tau) + (10**pKA))

#Full agonist best fit
#select file
dialog = wx.FileDialog(None, "Choose full-agonist dat file", os.getcwd(), "","*.dat", wx.FD_OPEN)
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
    res.write("Functional response - Operational Model\n\n")
    res.write("# tau\tEmax\tpKA\tData file\n")
    #prepare file for Grace plot
    if os.path.isfile("FR_OM_PA.draw"):
        os.remove("FR_OM_PA.draw")
    draw = open("FR_OM_PA.draw","w")
    c=-1 #plot counter
    d=0  #symbolcounter
    #initial best fit for full agonist
    i = -1
    res.write("\nFull agonist best fit\n")
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
            pKA_estim = x_min + (x_max - x_min) * 0.5
            pKA_min = x_min
            pKA_max = x_max - 0.5
            Emax_estim = basal + (y_max - basal) * 2
            Emax_min = basal + (Emax_estim - basal) * 0.1
            Emax_max = basal + (Emax_estim - basal) * 10
            tau_estim = 1
            tau_min = 0.001
            tau_max = 1000
            p1 = [tau_estim, Emax_estim, pKA_estim]
            #fit data
            p1_opt, p1_cov = opt.curve_fit(func, x_data_1, y_data_1, p1, bounds=([tau_min, Emax_min, pKA_min],[tau_max,Emax_max, pKA_max]))
            p1_err = np.sqrt(np.diag(p1_cov))
            tau_calc = (p1_opt[0])
            Emax_calc = (p1_opt[1])
            pKA_calc = (p1_opt[2])
            tau_err = (p1_err[0])
            Emax_err = (p1_err[1])
            pKA_err = (p1_err[2])
            #write results
            tau_res = (str("{0:.4f}".format(tau_calc))+' ± '+str("{0:.4f}".format(tau_err)))
            Emax_res = (str("{0:.2f}".format(Emax_calc))+' ± '+str("{0:.2f}".format(Emax_err)))
            pKA_res = (str("{0:.2f}".format(pKA_calc))+' ± '+str("{0:.2f}".format(pKA_err)))
            res.write(str(tau_res)+"\t"+str(Emax_res)+"\t"+str(pKA_res)+"\t"+str(file_1)+"\n")
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
            draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau_calc))+' \\#{B1} '+str("{0:.4f}".format(tau_err))+"; E\\sMAX\\N="+str("{0:.2f}".format(Emax_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax_err))+"; pK\\sA\\N="+str("{0:.2f}".format(pKA_calc))+' \\#{B1} '+str("{0:.2f}".format(pKA_err))+"; "+str(file_1)+"\" \n")
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

#Partial agonist best fit
#select file
dialog = wx.FileDialog(None, "Choose partial-agonist dat file", os.getcwd(), "","*.dat", wx.FD_OPEN)
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
    #initial best fit for partial agonist
    path_2, file_2=os.path.split(selected_2)
    base_2=os.path.splitext(selected_2)[0]
    res.write("\nPartial agonist best fit\n")
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
            pKA_estim = x_min + (x_max - x_min) * 0.5
            pKA_min = x_min
            pKA_max = x_max - 0.5
            Emax_estim = (y_max -1) * 2
            Emax_min = 1 + (Emax_estim -1) * 0.1
            Emax_max = 1 + (Emax_estim -1) * 10
            tau_estim = 0.5
            tau_min = 0.001
            tau_max = 1000
            p2 = [tau_estim, Emax_estim, pKA_estim]
            #fit data
            p2_opt, p2_cov = opt.curve_fit(func, x_data_2, y_data_2, p2, bounds=([tau_min, Emax_min, pKA_min],[tau_max,Emax_max, pKA_max]))
            p2_err = np.sqrt(np.diag(p2_cov))
            tau_calc = (p2_opt[0])
            Emax_calc = (p2_opt[1])
            pKA_calc = (p2_opt[2])
            tau_err = (p2_err[0])
            Emax_err = (p2_err[1])
            pKA_err = (p2_err[2])
            #write results
            tau_res = (str("{0:.4f}".format(tau_calc))+' ± '+str("{0:.4f}".format(tau_err)))
            Emax_res = (str("{0:.2f}".format(Emax_calc))+' ± '+str("{0:.2f}".format(Emax_err)))
            pKA_res = (str("{0:.2f}".format(pKA_calc))+' ± '+str("{0:.2f}".format(pKA_err)))
            res.write(str(tau_res)+"\t"+str(Emax_res)+"\t"+str(pKA_res)+"\t"+str(file_2)+"\n")
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
            draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau_calc))+' \\#{B1} '+str("{0:.4f}".format(tau_err))+"; E\\sMAX\\N="+str("{0:.2f}".format(Emax_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax_err))+"; pK\\sA\\N="+str("{0:.2f}".format(pKA_calc))+' \\#{B1} '+str("{0:.2f}".format(pKA_err))+"; "+str(file_2)+"\" \n")
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
    
#Global fit
if np.any(x_data_1 != x_data_2):
    msg = ('X-data differ between sets.\nGlobal fit will not be performed\n')
    errors = errors + msg
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
else:
    res.write("\nGlobal fit with shared Emax\n")
    #fit data
    def func2(x, p):
        tau, Emax, pKA = p
        return basal + ((10**x) * tau * (Emax - basal)) / ((10**x) * (1 +tau) + (10**pKA))
    def err(p, x, y):
        return func2(x, p) - y
    def err_global(p, x, y1, y2):
        # p is now a_1, b, c_1, a_2, c_2, with b shared between the two
        p_1 = p[0], p[1], p[2]
        p_2 = p[3], p[1], p[4]
        err1 = err(p_1, x, y1)
        err2 = err(p_2, x, y2)
        return np.concatenate((err1, err2))
    pg_estim = [p1_opt[0], p1_opt[1], p1_opt[2], p2_opt[0], p2_opt[2]]
    pg_opt, cov_x, infodict, errmsg, success = opt.leastsq(err_global, pg_estim, args=(x_data_1, y_data_1, y_data_2), full_output=1, epsfcn=0.0001)
    residuals = err_global(pg_opt, x_data_1, y_data_1, y_data_2)
    reduced_chi_square = np.sum(residuals**2)/(len(x_data_1)-2)
    pg_cov = cov_x * reduced_chi_square
    pg_err = np.sqrt(np.diag(pg_cov))
    pg1_opt = [pg_opt[0], pg_opt[1], pg_opt[2]]
    pg2_opt = [pg_opt[3], pg_opt[1],pg_opt[4]]
    tau1_calc = (pg_opt[0])
    tau1_err = (pg_err[0])
    Emax1_calc = (pg_opt[1])
    Emax1_err = (pg_err[1])
    pKA1_calc = (pg_opt[2])
    pKA1_err = (pg_err[2])
    tau2_calc = (pg_opt[3])
    tau2_err = (pg_err[3])
    Emax2_calc = (pg_opt[1])
    Emax2_err = (pg_err[1])
    pKA2_calc = (pg_opt[4])
    pKA2_err = (pg_err[4])
    #write results
    tau1_res = (str("{0:.4f}".format(tau1_calc))+' ± '+str("{0:.4f}".format(tau1_err)))
    Emax1_res = (str("{0:.2f}".format(Emax1_calc))+' ± '+str("{0:.2f}".format(Emax1_err)))
    pKA1_res = (str("{0:.2f}".format(pKA1_calc))+' ± '+str("{0:.2f}".format(pKA1_err)))
    res.write(str(tau1_res)+"\t"+str(Emax1_res)+"\t"+str(pKA1_res)+"\t"+str(file_1)+"\n")
    tau2_res = (str("{0:.4f}".format(tau2_calc))+' ± '+str("{0:.4f}".format(tau2_err)))
    Emax2_res = (str("{0:.2f}".format(Emax2_calc))+' ± '+str("{0:.2f}".format(Emax2_err)))
    pKA2_res = (str("{0:.2f}".format(pKA2_calc))+' ± '+str("{0:.2f}".format(pKA2_err)))
    res.write(str(tau2_res)+"\t"+str(Emax2_res)+"\t"+str(pKA2_res)+"\t"+str(file_2)+"\n")
    #calculate curve full agonist curve
    x_calc = np.arange(x_min, x_max, step)
    y_calc = func(x_calc, pg1_opt)
    xy_calc = np.column_stack((x_calc, y_calc))
    #write Grace plot
    c=(c+1)
    fit=(str(base_1)+'_FR_OM_PA_gfit.data')
    draw.write("read xy \""+str(fit)+"\" \n")
    draw.write("s"+str(c)+" symbol 0 \n")
    draw.write("s"+str(c)+" line type 1 \n")
    draw.write("s"+str(c)+" line linestyle 2 \n")
    draw.write("s"+str(c)+" line linewidth 2 \n")
    draw.write("s"+str(c)+" line color 2 \n")
    draw.write("s"+str(c)+" layer 51 \n")
    draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau1_calc))+' \\#{B1} '+str("{0:.4f}".format(tau1_err))+"; E\\sMAX\\N="+str("{0:.2f}".format(Emax1_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax1_err))+"; pK\\sA\\N="+str("{0:.2f}".format(pKA1_calc))+' \\#{B1} '+str("{0:.2f}".format(pKA1_err))+"; "+str(file_1)+"\" \n")
    
    np.savetxt(fit,xy_calc,fmt='%.4e')
    
    # add to plot
    plt.plot(x_calc, y_calc, 'y', linestyle='--')
    #calculate curve partial agonist curve
    x_calc = np.arange(x_min, x_max, step)
    y_calc = func(x_calc, pg2_opt)
    xy_calc = np.column_stack((x_calc, y_calc))
    #write Grace plot
    c=(c+1)
    fit=(str(base_2)+'_FR_OM_PA_gfit.data')
    draw.write("read xy \""+str(fit)+"\" \n")
    draw.write("s"+str(c)+" symbol 0 \n")
    draw.write("s"+str(c)+" line type 1 \n")
    draw.write("s"+str(c)+" line linestyle 2 \n")
    draw.write("s"+str(c)+" line linewidth 2 \n")
    draw.write("s"+str(c)+" line color 2 \n")
    draw.write("s"+str(c)+" layer 51 \n")
    draw.write("s"+str(c)+" legend \"\\f{Symbol}t\\f{}="+str("{0:.4f}".format(tau2_calc))+' \\#{B1} '+str("{0:.4f}".format(tau2_err))+"; E\\sMAX\\N="+str("{0:.2f}".format(Emax2_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax2_err))+"; pK\\sA\\N="+str("{0:.2f}".format(pKA2_calc))+' \\#{B1} '+str("{0:.2f}".format(pKA2_err))+"; "+str(file_2)+"\" \n")
    
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
