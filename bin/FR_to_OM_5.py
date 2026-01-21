#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:35:07 2016

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
import os
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
i = -1
x_min_min = 0
x_max_max = -15
y_max_max = 0

#get system basal
ask = ('Enter basal value to be substracted\nUsually:\n0 for fractional response\n1 for folds over basal')
dlg = wx.TextEntryDialog(None, ask,"Input",'0')
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
dialog = wx.FileDialog(None, "Choose dat file (1 of 5) to be analysed.", os.getcwd(), "","*.dat", wx.FD_OPEN)
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
    x_data_1 = data_1[:,0]
    y_data_1 = data_1[:,1]
    x_data_err_1 = data_1[:,2]
    y_data_err_1 = data_1[:,3]
    x_min_1 = np.amin(x_data_1)
    x_max_1 = np.amax(x_data_1)
    y_min_1 = np.amin(y_data_1)
    y_max_1 = np.amax(y_data_1)
    if np.size(x_data_1) < 4:
        msg = ('Too few data points in ' +str(selected_1)+ ' This data will be skipped\n')
        errors = errors + msg
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    else:
        if x_min_1 < -15 or x_max_1 > 0:
            msg = ('X value out of range ,<15,0>! '+str(selected_1)+' will be skipped\n')
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
            step_1 = (x_max_1 - x_min_1) * 0.01
            #get estimates & bounds
            Emax_estim = y_max_1
            Emax_min = y_max_1 * 0.5
            Emax_max = y_max_1 * 10
            pKA_estim = x_max_1 + 0.5
            pKA_min = x_max_1
            pKA_max = x_max_1 + 3
            #get basal value
            #fit data
            p1 = np.array([Emax_estim, pKA_estim])
            p1_opt, p1_cov = opt.curve_fit(func, x_data_1, y_data_1, p1, bounds=([Emax_min, pKA_min],[Emax_max, pKA_max]))
            p1_err = np.sqrt(np.diag(p1_cov))
            Emax1_calc = (p1_opt[0])
            pKA1_calc = (p1_opt[1])
            Emax1_err = (p1_err[0])
            pKA1_err = (p1_err[1])
            #write results
            head_1, tail_1 = os.path.split(selected_1)
            Emax1_res = (str("{0:.2f}".format(Emax1_calc))+' ± '+str("{0:.2f}".format(Emax1_err)))
            pKA1_res = (str("{0:.2f}".format(pKA1_calc))+' ± '+str("{0:.2f}".format(pKA1_err)))
            res.write(str(Emax1_res)+"\t"+str(pKA1_res)+"\t"+str(basal)+"\t"+str(tail_1)+"\n")
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
            draw.write("s"+str(c)+" legend \"E\\sMAX\\N = "+str("{0:.2f}".format(Emax1_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax1_err))+"; logK\\sA\\N = "+str("{0:.2f}".format(pKA1_calc))+' \\#{B1} '+str("{0:.2f}".format(pKA1_err))+"; basal = "+str(basal)+"; "+str(tail_1)+"\" \n")
            #calculate curve
            x_calc = np.arange(x_min_1, x_max_1, step_1)
            y_calc = func(x_calc, *p1_opt)
            xy_calc = np.column_stack((x_calc, y_calc))
            #save fit curve
            c=(c+1)
            e=(c-1)
            fit=(str(tail_1)+'_FR_to_OM_fit.data')
            draw.write("read xy \""+str(fit)+"\" \n")
            draw.write("s"+str(c)+" symbol 0 \n")
            draw.write("s"+str(c)+" line type 1 \n")
            draw.write("s"+str(c)+" line color 1 \n")
            draw.write("s"+str(c)+" layer 51 \n")
            draw.write("s"+str(c)+" legend off \n")
            
            np.savetxt(fit,xy_calc,fmt='%.4e')
            
            #get color
            i = i + 1
            if i == 7:
                msg = ("More than 7 data sets. Colors repeat.\n")
                errors = errors + msg
                dialog = wx.MessageDialog(self, msg, 'Warning', wx.OK)
                dialog.ShowModal()
                dialog.Destroy()
                i = i - 7
            color = (color_list[i])
            # plot
            plt.plot(x_calc, y_calc, color)
            plt.errorbar(x_data_1, y_data_1, xerr=x_data_err_1, yerr=y_data_err_1, fmt = color + "o")

#second data set
dialog = wx.FileDialog(None, "Choose dat file (2 of 5) to be analysed.", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected_2=dialog.GetPath()
    data_2 = np.loadtxt(selected_2)    
    columns = np.size((data_2)[0,:])
#test wheter we have data
if columns == 0:
    msg = ('Empty data file\n')
    errors = msg
    dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
else:
    # load data
    x_data_2 = data_2[:,0]
    y_data_2 = data_2[:,1]
    x_data_err_2 = data_2[:,2]
    y_data_err_2 = data_2[:,3]
    x_min_2 = np.amin(x_data_2)
    x_max_2 = np.amax(x_data_2)
    y_min_2 = np.amin(y_data_2)
    y_max_2 = np.amax(y_data_2)
    if np.size(x_data_2) < 4:
        msg = ('Too few data points in ' +str(selected_2)+ ' This data will be skipped\n')
        errors = errors + msg
        dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    else:
        if x_min_2 < -15 or x_max_2 > 0:
            msg = ('X value out of range ,<15,0>! '+str(selected_2)+' will be skipped\n')
            errors = errors + msg
            dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            if x_max_2 > x_max_max:
                x_max_max = x_max_2
            if x_min_2 < x_min_min:
                x_min_min = x_min_2
            if y_max_2 > y_max_max:
                y_max_max = y_max_2
            step_2 = (x_max_2 - x_min_2) * 0.01
            #get estimates & bounds
            Emax_estim = y_max_2
            Emax_min = y_max_2 * 0.5
            Emax_max = y_max_2 * 10
            pKA_estim = x_max_2 + 0.5
            pKA_min = x_max_2
            pKA_max = x_max_2 + 3
            #fit data
            p2 = np.array([Emax_estim, pKA_estim])
            p2_opt, p2_cov = opt.curve_fit(func, x_data_2, y_data_2, p2, bounds=([Emax_min, pKA_min],[Emax_max, pKA_max]))
            p2_err = np.sqrt(np.diag(p2_cov))
            Emax2_calc = (p2_opt[0])
            pKA2_calc = (p2_opt[1])
            Emax2_err = (p2_err[0])
            pKA2_err = (p2_err[1])
            #write results
            head_2, tail_2 = os.path.split(selected_2)
            Emax2_res = (str("{0:.2f}".format(Emax2_calc))+' ± '+str("{0:.2f}".format(Emax2_err)))
            pKA2_res = (str("{0:.2f}".format(pKA2_calc))+' ± '+str("{0:.2f}".format(pKA2_err)))
            res.write(str(Emax2_res)+"\t"+str(pKA2_res)+"\t"+str(basal)+"\t"+str(tail_2)+"\n")
            #write Grace plot
            c=(c+1)
            d=(d+1)
            draw.write("read xydxdy \""+str(selected_2)+"\" \n")
            draw.write("s"+str(c)+" symbol "+str(d)+" \n")
            draw.write("s"+str(c)+" symbol size 0.8 \n")
            draw.write("s"+str(c)+" symbol color 1 \n")
            draw.write("s"+str(c)+" symbol fill color 0 \n")
            draw.write("s"+str(c)+" symbol fill pattern 1 \n")
            draw.write("s"+str(c)+" errorbar color 1 \n")
            draw.write("s"+str(c)+" errorbar size 0.8 \n")
            draw.write("s"+str(c)+" line type 0 \n")
            draw.write("s"+str(c)+" legend \"E\\sMAX\\N = "+str("{0:.2f}".format(Emax2_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax2_err))+"; logK\\sA\\N = "+str("{0:.2f}".format(pKA2_calc))+' \\#{B1} '+str("{0:.2f}".format(pKA2_err))+"; basal = "+str(basal)+"; "+str(tail_2)+"\" \n")
            #calculate curve
            x_calc = np.arange(x_min_2, x_max_2, step_2)
            y_calc = func(x_calc, *p2_opt)
            xy_calc = np.column_stack((x_calc, y_calc))
            #save fit curve
            c=(c+1)
            e=(c-1)
            fit=(str(tail_2)+'_FR_to_OM_fit.data')
            draw.write("read xy \""+str(fit)+"\" \n")
            draw.write("s"+str(c)+" symbol 0 \n")
            draw.write("s"+str(c)+" line type 1 \n")
            draw.write("s"+str(c)+" line color 1 \n")
            draw.write("s"+str(c)+" layer 51 \n")
            draw.write("s"+str(c)+" legend off \n")
            
            np.savetxt(fit,xy_calc,fmt='%.4e')
            
            #get color
            i = i + 1
            if i == 7:
                msg = ("More than 7 data sets. Colors repeat.\n")
                errors = errors + msg
                dialog = wx.MessageDialog(self, msg, 'Warning', wx.OK)
                dialog.ShowModal()
                dialog.Destroy()
                i = i - 7
            color = (color_list[i])
            # plot
            plt.plot(x_calc, y_calc, color)
            plt.errorbar(x_data_2, y_data_2, xerr=x_data_err_2, yerr=y_data_err_2, fmt = color + "o")

#third data set
dialog = wx.FileDialog(None, "Choose dat file (3 of 5) to be analysed.", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected_3=dialog.GetPath()
    data_3 = np.loadtxt(selected_3)    
    columns = np.size((data_3)[0,:])
#test wheter we have data
if columns == 0:
    msg = ('Empty data file\n')
    errors = msg
    dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
else:
    # load data
    x_data_3 = data_3[:,0]
    y_data_3 = data_3[:,1]
    x_data_err_3 = data_3[:,2]
    y_data_err_3 = data_3[:,3]
    x_min_3 = np.amin(x_data_3)
    x_max_3 = np.amax(x_data_3)
    y_min_3 = np.amin(y_data_3)
    y_max_3 = np.amax(y_data_3)
    if np.size(x_data_3) < 4:
        msg = ('Too few data points in ' +str(selected_3)+ ' This data will be skipped\n')
        errors = errors + msg
        dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    else:
        if x_min_3 < -15 or x_max_3 > 0:
            msg = ('X value out of range ,<15,0>! '+str(selected_3)+' will be skipped\n')
            errors = errors + msg
            dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            if x_max_3 > x_max_max:
                x_max_max = x_max_3
            if x_min_3 < x_min_min:
                x_min_min = x_min_3
            if y_max_3 > y_max_max:
                y_max_max = y_max_3
            step_3 = (x_max_3 - x_min_3) * 0.01
            #get estimates & bounds
            Emax_estim = y_max_3
            Emax_min = y_max_3 * 0.5
            Emax_max = y_max_3 * 10
            pKA_estim = x_max_3 + 0.5
            pKA_min = x_max_3
            pKA_max = x_max_3 + 3
            #fit data
            p3 = np.array([Emax_estim, pKA_estim])
            p3_opt, p3_cov = opt.curve_fit(func, x_data_3, y_data_3, p3, bounds=([Emax_min, pKA_min],[Emax_max, pKA_max]))
            p3_err = np.sqrt(np.diag(p3_cov))
            Emax3_calc = (p3_opt[0])
            pKA3_calc = (p3_opt[1])
            Emax3_err = (p3_err[0])
            pKA3_err = (p3_err[1])
            #write results
            head_3, tail_3 = os.path.split(selected_3)
            Emax3_res = (str("{0:.2f}".format(Emax3_calc))+' ± '+str("{0:.2f}".format(Emax3_err)))
            pKA3_res = (str("{0:.2f}".format(pKA3_calc))+' ± '+str("{0:.2f}".format(pKA3_err)))
            res.write(str(Emax3_res)+"\t"+str(pKA3_res)+"\t"+str(basal)+"\t"+str(tail_3)+"\n")
            #write Grace plot
            c=(c+1)
            d=(d+1)
            draw.write("read xydxdy \""+str(selected_3)+"\" \n")
            draw.write("s"+str(c)+" symbol "+str(d)+" \n")
            draw.write("s"+str(c)+" symbol size 0.8 \n")
            draw.write("s"+str(c)+" symbol color 1 \n")
            draw.write("s"+str(c)+" symbol fill color 0 \n")
            draw.write("s"+str(c)+" symbol fill pattern 1 \n")
            draw.write("s"+str(c)+" errorbar color 1 \n")
            draw.write("s"+str(c)+" errorbar size 0.8 \n")
            draw.write("s"+str(c)+" line type 0 \n")
            draw.write("s"+str(c)+" legend \"E\\sMAX\\N = "+str("{0:.2f}".format(Emax3_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax3_err))+"; logK\\sA\\N = "+str("{0:.2f}".format(pKA3_calc))+' \\#{B1} '+str("{0:.2f}".format(pKA3_err))+"; basal = "+str(basal)+"; "+str(tail_3)+"\" \n")
            #calculate curve
            x_calc = np.arange(x_min_3, x_max_3, step_3)
            y_calc = func(x_calc, *p3_opt)
            xy_calc = np.column_stack((x_calc, y_calc))
            #save fit curve
            c=(c+1)
            e=(c-1)
            fit=(str(tail_3)+'_FR_to_OM_fit.data')
            draw.write("read xy \""+str(fit)+"\" \n")
            draw.write("s"+str(c)+" symbol 0 \n")
            draw.write("s"+str(c)+" line type 1 \n")
            draw.write("s"+str(c)+" line color 1 \n")
            draw.write("s"+str(c)+" layer 51 \n")
            draw.write("s"+str(c)+" legend off \n")
            
            np.savetxt(fit,xy_calc,fmt='%.4e')
            
            #get color
            i = i + 1
            if i == 7:
                msg = ("More than 7 data sets. Colors repeat.\n")
                errors = errors + msg
                dialog = wx.MessageDialog(self, msg, 'Warning', wx.OK)
                dialog.ShowModal()
                dialog.Destroy()
                i = i - 7
            color = (color_list[i])
            # plot
            plt.plot(x_calc, y_calc, color)
            plt.errorbar(x_data_3, y_data_3, xerr=x_data_err_3, yerr=y_data_err_3, fmt = color + "o")

#fourth data set
dialog = wx.FileDialog(None, "Choose dat file (4 of 5) to be analysed.", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected_4=dialog.GetPath()
    data_4 = np.loadtxt(selected_4)    
    columns = np.size((data_4)[0,:])
#test wheter we have data
if columns == 0:
    msg = ('Empty data file\n')
    errors = msg
    dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
else:
    # load data
    x_data_4 = data_4[:,0]
    y_data_4 = data_4[:,1]
    x_data_err_4 = data_4[:,2]
    y_data_err_4 = data_4[:,3]
    x_min_4 = np.amin(x_data_4)
    x_max_4 = np.amax(x_data_4)
    y_min_4 = np.amin(y_data_4)
    y_max_4 = np.amax(y_data_4)
    if np.size(x_data_4) < 4:
        msg = ('Too few data points in ' +str(selected_4)+ ' This data will be skipped\n')
        errors = errors + msg
        dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    else:
        if x_min_4 < -15 or x_max_4 > 0:
            msg = ('X value out of range ,<15,0>! '+str(selected_4)+' will be skipped\n')
            errors = errors + msg
            dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            if x_max_4 > x_max_max:
                x_max_max = x_max_4
            if x_min_4 < x_min_min:
                x_min_min = x_min_4
            if y_max_4 > y_max_max:
                y_max_max = y_max_4
            step_4 = (x_max_4 - x_min_4) * 0.01
            #get estimates & bounds
            Emax_estim = y_max_4
            Emax_min = y_max_4 * 0.5
            Emax_max = y_max_4 * 10
            pKA_estim = x_max_4 + 0.5
            pKA_min = x_max_4
            pKA_max = x_max_4 + 3
            #fit data
            p4 = np.array([Emax_estim, pKA_estim])
            p4_opt, p4_cov = opt.curve_fit(func, x_data_4, y_data_4, p4, bounds=([Emax_min, pKA_min],[Emax_max, pKA_max]))
            p4_err = np.sqrt(np.diag(p4_cov))
            Emax4_calc = (p4_opt[0])
            pKA4_calc = (p4_opt[1])
            Emax4_err = (p4_err[0])
            pKA4_err = (p4_err[1])
            #write results
            head_4, tail_4 = os.path.split(selected_4)
            Emax4_res = (str("{0:.2f}".format(Emax4_calc))+' ± '+str("{0:.2f}".format(Emax4_err)))
            pKA4_res = (str("{0:.2f}".format(pKA4_calc))+' ± '+str("{0:.2f}".format(pKA4_err)))
            res.write(str(Emax4_res)+"\t"+str(pKA4_res)+"\t"+str(basal)+"\t"+str(tail_4)+"\n")
            #write Grace plot
            c=(c+1)
            d=(d+1)
            draw.write("read xydxdy \""+str(selected_4)+"\" \n")
            draw.write("s"+str(c)+" symbol "+str(d)+" \n")
            draw.write("s"+str(c)+" symbol size 0.8 \n")
            draw.write("s"+str(c)+" symbol color 1 \n")
            draw.write("s"+str(c)+" symbol fill color 0 \n")
            draw.write("s"+str(c)+" symbol fill pattern 1 \n")
            draw.write("s"+str(c)+" errorbar color 1 \n")
            draw.write("s"+str(c)+" errorbar size 0.8 \n")
            draw.write("s"+str(c)+" line type 0 \n")
            draw.write("s"+str(c)+" legend \"E\\sMAX\\N = "+str("{0:.2f}".format(Emax4_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax4_err))+"; logK\\sA\\N = "+str("{0:.2f}".format(pKA4_calc))+' \\#{B1} '+str("{0:.2f}".format(pKA4_err))+"; basal = "+str(basal)+"; "+str(tail_4)+"\" \n")
            #calculate curve
            x_calc = np.arange(x_min_4, x_max_4, step_4)
            y_calc = func(x_calc, *p4_opt)
            xy_calc = np.column_stack((x_calc, y_calc))
            #save fit curve
            c=(c+1)
            e=(c-1)
            fit=(str(tail_4)+'_FR_to_OM_fit.data')
            draw.write("read xy \""+str(fit)+"\" \n")
            draw.write("s"+str(c)+" symbol 0 \n")
            draw.write("s"+str(c)+" line type 1 \n")
            draw.write("s"+str(c)+" line color 1 \n")
            draw.write("s"+str(c)+" layer 51 \n")
            draw.write("s"+str(c)+" legend off \n")
            
            np.savetxt(fit,xy_calc,fmt='%.4e')
            
            #get color
            i = i + 1
            if i == 7:
                msg = ("More than 7 data sets. Colors repeat.\n")
                errors = errors + msg
                dialog = wx.MessageDialog(self, msg, 'Warning', wx.OK)
                dialog.ShowModal()
                dialog.Destroy()
                i = i - 7
            color = (color_list[i])
            # plot
            plt.plot(x_calc, y_calc, color)
            plt.errorbar(x_data_4, y_data_4, xerr=x_data_err_4, yerr=y_data_err_4, fmt = color + "o")

#fifth data set
dialog = wx.FileDialog(None, "Choose dat file (5 of 5) to be analysed.", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected_5=dialog.GetPath()
    data_5 = np.loadtxt(selected_5)    
    columns = np.size((data_5)[0,:])
#test wheter we have data
if columns == 0:
    msg = ('Empty data file\n')
    errors = msg
    dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
else:
    # load data
    x_data_5 = data_5[:,0]
    y_data_5 = data_5[:,1]
    x_data_err_5 = data_5[:,2]
    y_data_err_5 = data_5[:,3]
    x_min_5 = np.amin(x_data_5)
    x_max_5 = np.amax(x_data_5)
    y_min_5 = np.amin(y_data_5)
    y_max_5 = np.amax(y_data_5)
    if np.size(x_data_5) < 4:
        msg = ('Too few data points in ' +str(selected_5)+ ' This data will be skipped\n')
        errors = errors + msg
        dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    else:
        if x_min_5 < -15 or x_max_5 > 0:
            msg = ('X value out of range ,<15,0>! '+str(selected_5)+' will be skipped\n')
            errors = errors + msg
            dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            if x_max_5 > x_max_max:
                x_max_max = x_max_5
            if x_min_5 < x_min_min:
                x_min_min = x_min_5
            if y_max_5 > y_max_max:
                y_max_max = y_max_5
            step_5 = (x_max_5 - x_min_5) * 0.01
            #get estimates & bounds
            Emax_estim = y_max_5
            Emax_min = y_max_5 * 0.5
            Emax_max = y_max_5 * 10
            pKA_estim = x_max_5 + 0.5
            pKA_min = x_max_5
            pKA_max = x_max_5 + 3
            #fit data
            p5 = np.array([Emax_estim, pKA_estim])
            p5_opt, p5_cov = opt.curve_fit(func, x_data_5, y_data_5, p5, bounds=([Emax_min, pKA_min],[Emax_max, pKA_max]))
            p5_err = np.sqrt(np.diag(p5_cov))
            Emax5_calc = (p5_opt[0])
            pKA5_calc = (p5_opt[1])
            Emax5_err = (p5_err[0])
            pKA5_err = (p5_err[1])
            #write results
            head_5, tail_5 = os.path.split(selected_5)
            Emax5_res = (str("{0:.2f}".format(Emax5_calc))+' ± '+str("{0:.2f}".format(Emax5_err)))
            pKA5_res = (str("{0:.2f}".format(pKA5_calc))+' ± '+str("{0:.2f}".format(pKA5_err)))
            res.write(str(Emax5_res)+"\t"+str(pKA5_res)+"\t"+str(basal)+"\t"+str(tail_5)+"\n")
            #write Grace plot
            c=(c+1)
            d=(d+1)
            draw.write("read xydxdy \""+str(selected_5)+"\" \n")
            draw.write("s"+str(c)+" symbol "+str(d)+" \n")
            draw.write("s"+str(c)+" symbol size 0.8 \n")
            draw.write("s"+str(c)+" symbol color 1 \n")
            draw.write("s"+str(c)+" symbol fill color 0 \n")
            draw.write("s"+str(c)+" symbol fill pattern 1 \n")
            draw.write("s"+str(c)+" errorbar color 1 \n")
            draw.write("s"+str(c)+" errorbar size 0.8 \n")
            draw.write("s"+str(c)+" line type 0 \n")
            draw.write("s"+str(c)+" legend \"E\\sMAX\\N = "+str("{0:.2f}".format(Emax5_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax5_err))+"; logK\\sA\\N = "+str("{0:.2f}".format(pKA5_calc))+' \\#{B1} '+str("{0:.2f}".format(pKA5_err))+"; basal = "+str(basal)+"; "+str(tail_5)+"\" \n")
            #calculate curve
            x_calc = np.arange(x_min_5, x_max_5, step_5)
            y_calc = func(x_calc, *p5_opt)
            xy_calc = np.column_stack((x_calc, y_calc))
            #save fit curve
            c=(c+1)
            e=(c-1)
            fit=(str(tail_5)+'_FR_to_OM_fit.data')
            draw.write("read xy \""+str(fit)+"\" \n")
            draw.write("s"+str(c)+" symbol 0 \n")
            draw.write("s"+str(c)+" line type 1 \n")
            draw.write("s"+str(c)+" line color 1 \n")
            draw.write("s"+str(c)+" layer 51 \n")
            draw.write("s"+str(c)+" legend off \n")
            
            np.savetxt(fit,xy_calc,fmt='%.4e')
            
            #get color
            i = i + 1
            if i == 7:
                msg = ("More than 7 data sets. Colors repeat.\n")
                errors = errors + msg
                dialog = wx.MessageDialog(None, msg, 'Warning', wx.OK)
                dialog.ShowModal()
                dialog.Destroy()
                i = i - 7
            color = (color_list[i])
            # plot
            plt.plot(x_calc, y_calc, color)
            plt.errorbar(x_data_5, y_data_5, xerr=x_data_err_5, yerr=y_data_err_5, fmt = color + "o")

#Global fit
res.write("\nGlobal fit with shared Emax \n")
#fit data
def func2(x, p):
    pKA, Emax = p
    return basal + (Emax - basal) - (((Emax-basal)*(10**x)) / (10**pKA))

def err(p, x, y):
    return func2(x, p) - y

def err_global(p, x1, x2, x3, x4, x5, y1, y2, y3, y4, y5):
    p_1 = p[0], p[1]
    p_2 = p[2], p[1]
    p_3 = p[3], p[1]
    p_4 = p[4], p[1]
    p_5 = p[5], p[1]
    err1 = err(p_1, x1, y1)
    err2 = err(p_2, x2, y2)
    err3 = err(p_3, x3, y3)
    err4 = err(p_4, x4, y4)
    err5 = err(p_5, x5, y5)
    return np.concatenate((err1, err2, err3, err4, err5))
pg_estim = [p1_opt[1], p1_opt[0], p2_opt[1], p3_opt[1], p4_opt[1], p5_opt[1]]
pg_opt, pg_cov, infodict, errmsg, success = opt.leastsq(err_global, pg_estim, args=(x_data_1, x_data_2, x_data_3, x_data_4, x_data_5, y_data_1, y_data_2, y_data_3, y_data_4, y_data_5), full_output=1, epsfcn=0.0001)
pg_err = np.sqrt(np.diag(pg_cov))
pg1_opt = [pg_opt[0], pg_opt[1]]
pg2_opt = [pg_opt[2], pg_opt[1]]
pg3_opt = [pg_opt[3], pg_opt[1]]
pg4_opt = [pg_opt[4], pg_opt[1]]
pg5_opt = [pg_opt[5], pg_opt[1]]
Emax1_calc = (pg_opt[1])
Emax1_err = (pg_err[1])
pKA1_calc = (pg_opt[0])
pKA1_err = (pg_err[0])
Emax2_calc = (pg_opt[1])
Emax2_err = (pg_err[1])
pKA2_calc = (pg_opt[2])
pKA2_err = (pg_err[2])
Emax3_calc = (pg_opt[1])
Emax3_err = (pg_err[1])
pKA3_calc = (pg_opt[3])
pKA3_err = (pg_err[3])
Emax4_calc = (pg_opt[1])
Emax4_err = (pg_err[1])
pKA4_calc = (pg_opt[4])
pKA4_err = (pg_err[4])
Emax5_calc = (pg_opt[1])
Emax5_err = (pg_err[1])
pKA5_calc = (pg_opt[5])
pKA5_err = (pg_err[5])
#write results
Emax1_res = (str("{0:.2f}".format(Emax1_calc))+' ± '+str("{0:.2f}".format(Emax1_err)))
pKA1_res = (str("{0:.2f}".format(pKA1_calc))+' ± '+str("{0:.2f}".format(pKA1_err)))
res.write(str(Emax1_res)+"\t"+str(pKA1_res)+"\t"+str(basal)+"\t"+str(tail_1)+"\n")
Emax2_res = (str("{0:.2f}".format(Emax2_calc))+' ± '+str("{0:.2f}".format(Emax2_err)))
pKA2_res = (str("{0:.2f}".format(pKA2_calc))+' ± '+str("{0:.2f}".format(pKA2_err)))
res.write(str(Emax2_res)+"\t"+str(pKA2_res)+"\t"+str(basal)+"\t"+str(tail_2)+"\n")
Emax3_res = (str("{0:.2f}".format(Emax3_calc))+' ± '+str("{0:.2f}".format(Emax3_err)))
pKA3_res = (str("{0:.2f}".format(pKA3_calc))+' ± '+str("{0:.2f}".format(pKA3_err)))
res.write(str(Emax3_res)+"\t"+str(pKA3_res)+"\t"+str(basal)+"\t"+str(tail_3)+"\n")
Emax4_res = (str("{0:.2f}".format(Emax4_calc))+' ± '+str("{0:.2f}".format(Emax4_err)))
pKA4_res = (str("{0:.2f}".format(pKA4_calc))+' ± '+str("{0:.2f}".format(pKA4_err)))
res.write(str(Emax4_res)+"\t"+str(pKA4_res)+"\t"+str(basal)+"\t"+str(tail_4)+"\n")
Emax5_res = (str("{0:.2f}".format(Emax5_calc))+' ± '+str("{0:.2f}".format(Emax5_err)))
pKA5_res = (str("{0:.2f}".format(pKA5_calc))+' ± '+str("{0:.2f}".format(pKA5_err)))
res.write(str(Emax5_res)+"\t"+str(pKA5_res)+"\t"+str(basal)+"\t"+str(tail_5)+"\n")
#calculate curve 1
x_calc = np.arange(x_min_1, x_max_1, step_1)
y_calc = func(x_calc, pg1_opt)
xy_calc = np.column_stack((x_calc, y_calc))
#write Grace plot curve 1
c=(c+1)
fit=(str(tail_1)+'_FR_to_OM_gfit.data')
draw.write("read xy \""+str(fit)+"\" \n")
draw.write("s"+str(c)+" symbol 0 \n")
draw.write("s"+str(c)+" line type 1 \n")
draw.write("s"+str(c)+" line linestyle 2 \n")
draw.write("s"+str(c)+" line linewidth 2 \n")
draw.write("s"+str(c)+" line color 2 \n")
draw.write("s"+str(c)+" layer 51 \n")
draw.write("s"+str(c)+" legend \"E\\sMAX\\N = "+str("{0:.2f}".format(Emax1_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax1_err))+"; logK\\sA\\N = "+str("{0:.2f}".format(pKA1_calc))+' \\#{B1} '+str("{0:.2f}".format(pKA1_err))+"; basal = "+str("{0:.2f}".format(basal))+"; "+str(tail_1)+"\" \n")

np.savetxt(fit,xy_calc,fmt='%.4e')

# add to plot
plt.plot(x_calc, y_calc, 'y', linestyle='--')
#calculate  curve 2
x_calc = np.arange(x_min_2, x_max_2, step_2)
y_calc = func(x_calc, pg2_opt)
xy_calc = np.column_stack((x_calc, y_calc))
#write Grace plot curve 2
c=(c+1)
fit=(str(tail_2)+'_FR_to_OM_gfit.data')
draw.write("read xy \""+str(fit)+"\" \n")
draw.write("s"+str(c)+" symbol 0 \n")
draw.write("s"+str(c)+" line type 1 \n")
draw.write("s"+str(c)+" line linestyle 2 \n")
draw.write("s"+str(c)+" line linewidth 2 \n")
draw.write("s"+str(c)+" line color 2 \n")
draw.write("s"+str(c)+" layer 51 \n")
draw.write("s"+str(c)+" legend \"E\\sMAX\\N = "+str("{0:.2f}".format(Emax2_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax2_err))+"; logK\\sA\\N ="+str("{0:.2f}".format(pKA2_calc))+' \\#{B1} '+str("{0:.2f}".format(pKA2_err))+"; basal = "+str("{0:.2f}".format(basal))+"; "+str(tail_2)+"\" \n")

np.savetxt(fit,xy_calc,fmt='%.4e')

# add to plot
plt.plot(x_calc, y_calc, 'y', linestyle='--')
#calculate  curve 3
x_calc = np.arange(x_min_3, x_max_3, step_3)
y_calc = func(x_calc, pg3_opt)
xy_calc = np.column_stack((x_calc, y_calc))
#write Grace plot curve 3
c=(c+1)
fit=(str(tail_3)+'_FR_to_OM_gfit.data')
draw.write("read xy \""+str(fit)+"\" \n")
draw.write("s"+str(c)+" symbol 0 \n")
draw.write("s"+str(c)+" line type 1 \n")
draw.write("s"+str(c)+" line linestyle 2 \n")
draw.write("s"+str(c)+" line linewidth 2 \n")
draw.write("s"+str(c)+" line color 2 \n")
draw.write("s"+str(c)+" layer 51 \n")
draw.write("s"+str(c)+" legend \"E\\sMAX\\N = "+str("{0:.2f}".format(Emax3_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax3_err))+"; logK\\sA\\N ="+str("{0:.2f}".format(pKA3_calc))+' \\#{B1} '+str("{0:.2f}".format(pKA3_err))+"; basal = "+str("{0:.2f}".format(basal))+"; "+str(tail_3)+"\" \n")

np.savetxt(fit,xy_calc,fmt='%.4e')

# add to plot
plt.plot(x_calc, y_calc, 'y', linestyle='--')
#calculate  curve 4
x_calc = np.arange(x_min_4, x_max_4, step_4)
y_calc = func(x_calc, pg4_opt)
xy_calc = np.column_stack((x_calc, y_calc))
#write Grace plot curve 4
c=(c+1)
fit=(str(tail_4)+'_FR_to_OM_gfit.data')
draw.write("read xy \""+str(fit)+"\" \n")
draw.write("s"+str(c)+" symbol 0 \n")
draw.write("s"+str(c)+" line type 1 \n")
draw.write("s"+str(c)+" line linestyle 2 \n")
draw.write("s"+str(c)+" line linewidth 2 \n")
draw.write("s"+str(c)+" line color 2 \n")
draw.write("s"+str(c)+" layer 51 \n")
draw.write("s"+str(c)+" legend \"E\\sMAX\\N = "+str("{0:.2f}".format(Emax4_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax4_err))+"; logK\\sA\\N ="+str("{0:.2f}".format(pKA4_calc))+' \\#{B1} '+str("{0:.2f}".format(pKA4_err))+"; basal = "+str("{0:.2f}".format(basal))+"; "+str(tail_4)+"\" \n")

np.savetxt(fit,xy_calc,fmt='%.4e')

# add to plot
plt.plot(x_calc, y_calc, 'y', linestyle='--')
#calculate  curve 5
x_calc = np.arange(x_min_5, x_max_5, step_5)
y_calc = func(x_calc, pg5_opt)
xy_calc = np.column_stack((x_calc, y_calc))
#write Grace plot curve 5
c=(c+1)
fit=(str(tail_5)+'_FR_to_OM_gfit.data')
draw.write("read xy \""+str(fit)+"\" \n")
draw.write("s"+str(c)+" symbol 0 \n")
draw.write("s"+str(c)+" line type 1 \n")
draw.write("s"+str(c)+" line linestyle 2 \n")
draw.write("s"+str(c)+" line linewidth 2 \n")
draw.write("s"+str(c)+" line color 2 \n")
draw.write("s"+str(c)+" layer 51 \n")
draw.write("s"+str(c)+" legend \"E\\sMAX\\N = "+str("{0:.2f}".format(Emax5_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax5_err))+"; logK\\sA\\N ="+str("{0:.2f}".format(pKA5_calc))+' \\#{B1} '+str("{0:.2f}".format(pKA5_err))+"; basal = "+str("{0:.2f}".format(basal))+"; "+str(tail_5)+"\" \n")

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
log.write(errors)
log.close()
