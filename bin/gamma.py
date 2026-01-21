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
x_min_min = 0
x_max_max = -15
y_max_max = 100

msg = ('This analysis only tests wheter competitor competes also with allosteric ligand, is bitopic.\n')
err = msg
dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
dialog.ShowModal()
dialog.Destroy()

#test wheter we have files
count = len(glob.glob('*.dat'))
if count == 0:
    msg = ('No .dat files found!\n')
    err = msg
    dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
else:
    #prepare file for writing results
    if os.path.isfile("gamma.res"):
        os.remove("gamma.res")
    res = open("gamma.res","w")
    res.write("Interaction of 3 ligands:\ntracer, bitopic, allosteric\n\n")
    res.write("KA\t\talpha\tKD\t\t[X]\t\tKL\t\t[L]\t\tP\t\tData file\n")
    #prepare file for Grace plot
    if os.path.isfile("gamma.draw"):
        os.remove("gamma.draw")
    draw = open("gamma.draw","w")
    c=-1 #plot counter
    d=0 #symbolcounter
    
    for file in glob.glob('*.dat'):
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
        if np.size(x_data) < 7 or (x_max - x_min) < 4:
            msg = ('Too few data points in ' +str(file)+ ' This data will be skipped\n')
            err = err + msg
            dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            if x_min < -15 or x_max > 0:
                msg = ('X value out of range ,<15,0>! '+str(file)+' will be skipped\n')
                err = err + msg
                dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
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
                #get tracer KD and concentration
                ask = ('Enter tracer KD for ' +str(file)+'\n')
                dlg = wx.TextEntryDialog(self, ask, defaultValue='500e-12')
                if dlg.ShowModal() == wx.ID_OK:
                    KD = dlg.GetValue()
                dlg.Destroy()
                ask = ('Enter tracer concentration for ' +str(file)+'\n')
                dlg = wx.TextEntryDialog(self, ask, defaultValue='200e-12')
                if dlg.ShowModal() == wx.ID_OK:
                    CX = dlg.GetValue()
                dlg.Destroy()            
                #get competitor KD and concentration
                ask = ('Enter competitor KL for ' +str(file)+'\n')
                dlg = wx.TextEntryDialog(self, ask, defaultValue='2e-6')
                if dlg.ShowModal() == wx.ID_OK:
                    KL = dlg.GetValue()
                dlg.Destroy()
                ask = ('Enter competitor concentration for ' +str(file)+'\n')
                dlg = wx.TextEntryDialog(self, ask, defaultValue='3e-6')
                if dlg.ShowModal() == wx.ID_OK:
                    CL = dlg.GetValue()
                dlg.Destroy()            
                #get KA and alpha of allosteric modulator
                ask = ('Enter KA of allosteric modulator\n for ' +str(file)+'\n')
                dlg = wx.TextEntryDialog(self, ask, defaultValue='2.7e-6')
                if dlg.ShowModal() == wx.ID_OK:
                    KA = dlg.GetValue()
                dlg.Destroy()
                ask = ('Enter cooperativity factor alpha\n for ' +str(file)+'\n')
                dlg = wx.TextEntryDialog(self, ask, defaultValue='0.3')
                if dlg.ShowModal() == wx.ID_OK:
                    alpha = dlg.GetValue()
                dlg.Destroy()
                #extract variables
                KD = float(KD)
                CX = float(CX)
                KL = float(KL)
                CL = float(CL)
                KA = float(KA)
                alpha = float(alpha)
                #calculate runs test
                y_rt = 100 * (KD + CX) / (CX + KD *(CL * KA + KL * (KA + 10**x_data)) / (KL * (KA + (10**x_data)/alpha)))
                y_dif = []
                for j in range(0,np.size(y_data)):
                    if y_data[j] > y_rt[j]:
                        y_dif.append(1)
                    else:
                        y_dif.append(0)
                n = np.size(y_dif)
                n1 = np.sum(y_dif)
                n2 = (n - n1)
                runs = 0
                for k in range(0,np.size(y_dif)-1):
                    if y_dif[k] != y_dif[k+1]:
                        runs = (runs + 1)
                    else:
                        runs = (runs + 0)
                mean = (2*n1*n2/n + 1)
                sd = np.sqrt(2*n1*n2*(2*n1*n2-n1-n2)/((n1+n2)**2)/(n1+n2-1))
                z = np.abs(runs-mean)/sd
                p = 2*(1-norm.cdf(z))
                if p < 0.05 or p == 'nan':
                    msg = ('Runs test failed for ' +str(file)+ '\nEither model does not fit or entered parameters are wrong.\n')
                    err = err + msg
                    dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
                    dialog.ShowModal()
                    dialog.Destroy()
                #write results
                res.write(str(KA)+"\t"+str(alpha)+"\t\t"+str(KD)+"\t"+str(CX)+"\t"+str(KL)+"\t"+str(CL)+"\t"+str("{0:.3f}".format(p))+"\t"+str(file)+"\n")
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
                draw.write("s"+str(c)+" legend \"P="+str("{0:.3f}".format(p))+"; "+str(base)+"\" \n")
                #calculate curve
                x_calc = np.arange(x_min, x_max, step)
                y_calc = 100 * (KD + CX) / (CX + KD *(CL * KA + KL * (KA + 10**x_calc)) / (KL * (KA + (10**x_calc)/alpha)))
                xy_calc = np.column_stack((x_calc, y_calc))
                #save fit curve
                c=(c+1)
                e=(c-1)
                fit=(str(base)+'_gamma_fit.data')
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
                    err = err + msg
                    dialog = wx.MessageDialog(self, msg, 'Warning', wx.OK)
                    dialog.ShowModal()
                    dialog.Destroy()
                    i = i - 7
                color = (color_list[i])
                # plot
                plt.plot(x_calc, y_calc, color)
                plt.errorbar(x_data, y_data, xerr=None, yerr=y_data_err, fmt = color + "o")
    
    now = time.strftime("%d.%m.%Y %H:%M:%S")
    res.write("\n\n"+str(now)+"\n")
    res.close()
    #Plot
    ax_min = x_min_min - 0.5
    ax_max = x_max_max + 0.5
    ay_max = y_max_max * 1.1
    plt.title("If it fits it is bitopic")
    plt.axis([ax_min,ax_max,0,ay_max])
    plt.xlabel("allosteric modulator [log c]")
    plt.ylabel("binding [% of control]")
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
