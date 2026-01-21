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
j = -1
x_min_min = 0
x_max_max = -15
y_max_max = 100

#initiate 3d data
data_3d = np.array([0,0,0,0])

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
    if os.path.isfile("allosteric_2_2.res"):
        os.remove("allosteric_2_2.res")
    res = open("allosteric_2_2.res","w")
    res.write("Allosteric interaction\n\n")
    #prepare file for Grace plot
    if os.path.isfile("alloster_2_2.draw"):
        os.remove("alloster_2_2.draw")
    draw = open("alloster_2_2.draw","w")
    c=-1 #plot counter
    d=0 #symbolcounter
    #get tracer KA and concentration
    ask = ('Enter KA value of tracer\n')
    dlg = wx.TextEntryDialog(None, ask, "Input",'250e-12')
    if dlg.ShowModal() == wx.ID_OK:
        KA = dlg.GetValue()
    dlg.Destroy()
    ask = ('Enter tracer concentration\n')
    dlg = wx.TextEntryDialog(None, ask, "Input",'100e-12')
    if dlg.ShowModal() == wx.ID_OK:
        CA = dlg.GetValue()
    dlg.Destroy()            
    #get parameters of the first modulator
    ask = ('Enter KB value of the first allosteric modulator\n(x-axis)\n')
    dlg = wx.TextEntryDialog(None, ask, "Input",'1e-8')
    if dlg.ShowModal() == wx.ID_OK:
        KB = dlg.GetValue()
    dlg.Destroy()
    ask = ('Enter alpha value\nTracer and the first modulator')
    dlg = wx.TextEntryDialog(None, ask, "Input",'0.2')
    if dlg.ShowModal() == wx.ID_OK:
        alpha = dlg.GetValue()
    dlg.Destroy()            
    #get parameters of the second modulator
    ask = ('Enter KC value of the second allosteric modulator\n(Fixed concentration)\n')
    dlg = wx.TextEntryDialog(None, ask, "Input",'1e-6')
    if dlg.ShowModal() == wx.ID_OK:
        KC = dlg.GetValue()
    dlg.Destroy()
    ask = ('Enter beta value\nTracer and the second modulator')
    dlg = wx.TextEntryDialog(None, ask, "Input",'10')
    if dlg.ShowModal() == wx.ID_OK:
        beta = dlg.GetValue()
    dlg.Destroy()
    res.write("KB="+str(KB)+"\nalpha="+str(alpha)+"\nKC="+str(KC)+"\nbeta="+str(beta)+"\nKA="+str(KA)+"\n[X]="+str(CA)+"\n")
    res.write("\ngamma\tdelta\t[B]\tData file\n")            
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
        if np.size(x_data) < 9 or (x_max - x_min) < 4:
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
                gamma_estim = 10
                gamma_min = 0.01
                gamma_max = 100
                delta_estim = 1
                delta_min = 0.1
                delta_max = 10
                ask = ('Enter concentration of B for ' +str(file)+'\n')
                dlg = wx.TextEntryDialog(None, ask, "Input",'1e-6')
                if dlg.ShowModal() == wx.ID_OK:
                    CC = dlg.GetValue()
                #fit data
                def func(x, gamma, delta):
                    global KA
                    KA = float(KA)
                    global CA
                    CA = float(CA)
                    global KB                    
                    KB = float(KB)
                    global alpha
                    alpha = float(alpha)
                    global KC
                    KC = float(KC)
                    global beta
                    beta = float(beta)
                    global CC
                    CC = float(CC)
                    return 100 * (CA + KA) / (CA + KA * (1 + (10**x) / KB + CC / KC * (1 + (10**x) / gamma / KB) ) / (1 + (10**x) / alpha / KB + CC / beta / KC * (1 + (10**x) / alpha / gamma / delta / KB ) ) )
                p0 = [gamma_estim, delta_estim]
                popt, pcov = opt.curve_fit(func, x_data, y_data, p0, bounds=([gamma_min,delta_min],[gamma_max,delta_max]))
                perr = np.sqrt(np.diag(pcov))
                gamma_calc = (popt[0])
                delta_calc = (popt[1])
                gamma_err = (perr[0])
                delta_err = (perr[1])
                #write results
                gamma_res = (str("{0:.2f}".format(gamma_calc))+' ± '+str("{0:.2f}".format(gamma_err)))
                delta_res = (str("{0:.2f}".format(delta_calc))+' ± '+str("{0:.2f}".format(delta_err)))
                res.write(str(gamma_res)+"\t"+str(delta_res)+"\t"+str(CC)+"\t"+str(file)+"\n")
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
                draw.write("s"+str(c)+" legend \"\\f{Symbol}g\\f{}="+str("{0:.2f}".format(gamma_calc))+" \\#{B1} "+str("{0:.2f}".format(gamma_err))+"; \\f{Symbol}d\\f{}="+str("{0:.2f}".format(delta_calc))+" \\#{B1} "+str("{0:.2f}".format(delta_err))+"; [B]="+str(CC)+"; "+str(base)+"\" \n")
                # add data to 3d
                j = j + 1
                CC_data = np.linspace(CC,CC,len(x_data))
                exec('data_3d_'+str(j)+' = np.stack((x_data, CC_data, y_data, y_data_err),axis=-1)')
                exec('data_3d = np.vstack((data_3d,data_3d_'+str(j)+'))')
                #calculate curve
                x_calc = np.arange(x_min, x_max, step)
                y_calc = func(x_calc, *popt)
                xy_calc = np.column_stack((x_calc, y_calc))
                #save fit curve
                c=(c+1)
                e=(c-1)
                fit=(str(base)+'_alloster_2_2_fit.data')
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
                
    #3D fit
    #load data
    data_3d=np.delete(data_3d,0,0)
    x_data_3d = data_3d[:,0]
    y_data_3d = data_3d[:,1]
    z_data_3d = data_3d[:,2]
    z_data_err = data_3d[:,3]
    global func_3d
    def func_3d(x, y, p):
        gamma, delta = p
        return 100 * (CA + KA) / (CA + KA * (1 + (10**x) / KB + y / KC * (1 + (10**x) / gamma / KB) ) / (1 + (10**x) / alpha / KB + y / beta / KC * (1 + (10**x) / alpha / gamma / delta / KB ) ) )
    def err_3d(p, x, y, z):
        return func_3d(x, y, p) - z
    
    pg_estim = popt
    pg_opt, cov_x, infodict, errmsg, success = opt.leastsq(err_3d, pg_estim, args=(x_data_3d, y_data_3d, z_data_3d), full_output=1, epsfcn=0.0001)
    residuals = err_3d(pg_opt, x_data_3d, y_data_3d, z_data_3d)
    reduced_chi_square = np.sum(residuals**2)/(len(x_data_3d)-2)
    pg_cov = cov_x * reduced_chi_square
    pg_err = np.sqrt(np.diag(pg_cov))
    gamma_calc = (pg_opt[0])
    gamma_err = (pg_err[0])
    delta_calc = (pg_opt[1])
    delta_err = (pg_err[1])
    gamma_res = (str("{0:.4f}".format(gamma_calc))+' ± '+str("{0:.4f}".format(gamma_err)))
    delta_res = (str("{0:.2f}".format(delta_calc))+' ± '+str("{0:.2f}".format(delta_err)))
    res.write("\n3D fit\ngamma\tdelta\n")
    res.write(str(gamma_res)+"\t"+str(delta_res)+"\n")
    #calculate curves and put them in the graph
    #same color for all
    d = d + 1
    for k in range(count):
        exec('x_3d_calc_'+str(k)+' = np.linspace(np.amin(data_3d_'+str(k)+'[:,0]),np.amax(data_3d_'+str(k)+'[:,0]),100)')
        exec('y_3d_'+str(k)+' = data_3d_'+str(k)+'[0,1]')
        exec('y_3d_calc_'+str(k)+' = np.linspace(y_3d_'+str(k)+',y_3d_'+str(k)+',100)')
        exec('z_3d_calc_'+str(k)+' = func_3d(x_3d_calc_'+str(k)+', y_3d_calc_'+str(k)+', pg_opt)')
        exec('xz_3d_calc_'+str(k)+' = np.column_stack((x_3d_calc_'+str(k)+', z_3d_calc_'+str(k)+'))')
        #save fit curve
        c=(c+1)
        fit=('data_3d_'+str(k)+'_fit.data')
        draw.write("read xy \""+str(fit)+"\" \n")
        draw.write("s"+str(c)+" symbol 0 \n")
        draw.write("s"+str(c)+" line type 1 \n")
        draw.write("s"+str(c)+" line color "+str(d)+" \n")
        draw.write("s"+str(c)+" layer 51 \n")
        draw.write("s"+str(c)+" legend on \n")
        draw.write("s"+str(c)+" legend \"\\f{Symbol}g\\f{}="+str("{0:.2f}".format(gamma_calc))+" \\#{B1} "+str("{0:.2f}".format(gamma_err))+"; \\f{Symbol}d\\f{}="+str("{0:.2f}".format(delta_calc))+" \\#{B1} "+str("{0:.2f}".format(delta_err))+"; 3D fit\" \n")
        fit=open(fit,'w')
        exec('np.savetxt(fit,xz_3d_calc_'+str(k)+',fmt=\"%.4e\")')
        fit.close()
        #add to plot
        exec('plt.plot(x_3d_calc_'+str(k)+', z_3d_calc_'+str(k)+', \"y\", linestyle=\"--\")')
    
    now = time.strftime("%d.%m.%Y %H:%M:%S")
    res.write("\n\n"+str(now)+"\n")
    res.close()
    #Plot
    ax_min = x_min_min - 0.5
    ax_max = x_max_max + 0.5
    ay_max = y_max_max * 1.1
    plt.title("Allosteric interaction")
    plt.axis([ax_min,ax_max,0,ay_max])
    plt.xlabel("allosteric modulator [log c]")
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
    draw.write("legend 0.08, 0.7 \n")
    draw.write("legend char size 0.8 \n")
    draw.write("legend font \"Helvetica\" \n")
    draw.close()

log = open("temp.log","w")
log.write(err)
log.close()
