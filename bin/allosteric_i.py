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

global CA, KA, KB_min, KB_estim, KB_max, alpha_min, alpha_estim, alpha_max

class Estimates(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE,
            useMetal=False,
            ):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, ID, title, pos, size, style)

        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, "Allosteric interaction - parameter estimates")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer = wx.GridSizer(3, 3, 5, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Tracer KA:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.KA = wx.TextCtrl(self, -1, str(KA), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.KA, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Tracer c:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.CA = wx.TextCtrl(self, -1, str(CA), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.CA, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "KB min:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.KB_min = wx.TextCtrl(self, -1, str(KB_min), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.KB_min, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "KB estimate:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.KB_estim = wx.TextCtrl(self, -1, str(KB_estim), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.KB_estim, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "KB max:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.KB_max = wx.TextCtrl(self, -1, str(KB_max), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.KB_max, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "alpha min:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.alpha_min = wx.TextCtrl(self, -1, str(alpha_min), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.alpha_min, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "alpha estimate:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.alpha_estim = wx.TextCtrl(self, -1, str(alpha_estim), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.alpha_estim, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "alpha max:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.alpha_max = wx.TextCtrl(self, -1, str(alpha_max), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.alpha_max, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)
        
        sizer.Add(grid_sizer, 1, 0, 10)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

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

#select file
dialog = wx.FileDialog(None, "Choose a data file", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    data = np.loadtxt(selected)    
    columns = np.size((data)[0,:])

#test wheter we have data
if columns == 0:
    msg = ('Empty data file\n')
    err = msg
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
else:
    #prepare file for writing results
    base=os.path.splitext(selected)[0]
    if os.path.isfile(str(base)+"_allosteric_i.res"):
        os.remove(str(base)+"_allosteric_i.res")
    res = open(str(base)+"_allosteric_i.res","w")
    res.write("Allosteric interaction\n\n")
    res.write("logKB\t\t\talpha\t\tKA\t\t[X]\t\tData file\n")
    #prepare file for Grace plot
    if os.path.isfile(str(base)+"_alloster_i.draw"):
        os.remove(str(base)+"_alloster_i.draw")
    draw = open(str(base)+"_alloster_i.draw","w")
    c=-1 #plot counter
    d=0 #symbolcounter
    
    # load data
    x_data = data[:,0]
    y_data = data[:,1]
    y_data_err = data[:,2]
    x_min = np.amin(x_data)
    x_max = np.amax(x_data)
    y_min = np.amin(y_data)
    y_max = np.amax(y_data)
    if np.size(x_data) < 6 or (x_max - x_min) < 3:
        msg = ('Too few data points in ' +str(base)+ ' This data will be skipped\n')
        err = err + msg
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    else:
        if x_min < -15 or x_max > 0:
            msg = ('X value out of range ,<15,0>! '+str(base)+' will be skipped\n')
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
            if (y_max - 100) > (100 - y_min):
                alpha_estim = 0.1
                alpha_min = 0.001
                alpha_max = 0.8
            else:
                alpha_estim = 5
                alpha_min = 1.2
                alpha_max = 1000
            KB_estim = (x_min + x_max) * 0.5
            KB_min = x_min + 0.5
            KB_max = x_max - 1
            CA = 100e-12
            KA = 250e-12
            dlg = Estimates(None, -1, "Enter values", size=(350, 200),
                           #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                           style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
                           )
            dlg.CenterOnScreen()
            val = dlg.ShowModal()
            if val == wx.ID_OK:
                CA = float(CA)
                KA = float(KA)
                KB_min = float(dlg.KB_min.GetValue())
                KB_estim = float(dlg.KB_estim.GetValue())
                KB_max = float(dlg.KB_max.GetValue())
                alpha_min = float(dlg.alpha_min.GetValue())
                alpha_estim = float(dlg.alpha_estim.GetValue())
                alpha_max = float(dlg.alpha_max.GetValue())
            else:
                msg = ('Analysis was canceled.')
                dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
                dialog.ShowModal()
                dialog.Destroy()
                log = open("temp.log","w")
                log.write("Error: Test was canceled")
                log.close()
                tolog = log.read()
                None.__log(tolog)
            dlg.Destroy()

            #fit data
            p0 = np.array([ KB_estim, alpha_estim])
            def func(x, KB, alpha):
                global CA, KA, KB_min, KB_estim, KB_max, alpha_min, alpha_estim, alpha_max
                CA = float(CA)
                KA = float(KA)
                KB_min = float(KB_min)
                KB_estim = float(KB_estim)
                KB_max = float(KB_max)
                alpha_min = float(alpha_min)
                alpha_estim = float(alpha_estim)
                alpha_max = float(alpha_max)
                return 100 * (CA + KA) / (CA + (KA * (10**KB + (10**x)))/(10**KB + (10**x)/alpha))
            popt, pcov = opt.curve_fit(func, x_data, y_data, p0, bounds=([KB_min, alpha_min],[KB_max, alpha_max]))
            perr = np.sqrt(np.diag(pcov))
            KB_calc = (popt[0])
            alpha_calc = (popt[1])
            KB_err = (perr[0])
            alpha_err = (perr[1])
            #write results
            KB_res = (str("{0:.2f}".format(KB_calc))+' ± '+str("{0:.2f}".format(KB_err)))
            if alpha_calc > 0:
                alpha_res = (str("{0:.2f}".format(alpha_calc))+' ± '+str("{0:.2f}".format(alpha_err)))
            else:
                alpha_res = (str("{0:.4f}".format(alpha_calc))+' ± '+str("{0:.4f}".format(alpha_err)))
            res.write(str(KB_res)+"\t"+str(alpha_res)+"\t"+str(KA)+"\t"+str(CA)+"\t"+str(base)+"\n")
            #write Grace plot
            c=(c+1)
            d=(d+1)
            base=os.path.splitext(base)[0]
            draw.write("read xydy \""+str(selected)+"\" \n")
            draw.write("s"+str(c)+" symbol "+str(d)+" \n")
            draw.write("s"+str(c)+" symbol size 0.8 \n")
            draw.write("s"+str(c)+" symbol color 1 \n")
            draw.write("s"+str(c)+" symbol fill color 0 \n")
            draw.write("s"+str(c)+" symbol fill pattern 1 \n")
            draw.write("s"+str(c)+" errorbar color 1 \n")
            draw.write("s"+str(c)+" errorbar size 0.8 \n")
            draw.write("s"+str(c)+" line type 0 \n")
            if alpha_calc > 0:
                draw.write("s"+str(c)+" legend \"logK\\sA\\N="+str("{0:.2f}".format(KB_calc))+' \\#{B1} '+str("{0:.2f}".format(KB_err))+"; \\f{Symbol}a\\f{}="+str("{0:.2f}".format(alpha_calc))+' \\#{B1} '+str("{0:.2f}".format(alpha_err))+";\\n\\n"+str(base)+"\" \n")
            else:
                draw.write("s"+str(c)+" legend \"logK\\sA\\N="+str("{0:.2f}".format(KB_calc))+' \\#{B1} '+str("{0:.2f}".format(KB_err))+"; \\f{Symbol}a\\f{}="+str("{0:.4f}".format(alpha_calc))+' \\#{B1} '+str("{0:.4f}".format(alpha_err))+";\\n\\n"+str(base)+"\" \n")
            #calculate fit
            y_fit = func(x_data, *popt)
            xy_fit = np.column_stack((x_data, y_fit))
            #save curve
            fit=(str(base)+'_alloster_i_fit.data')
            np.savetxt(fit,xy_fit,fmt='%.4e')
            #calculate curve
            x_curve = np.arange(x_min, x_max, step)
            y_curve = func(x_curve, *popt)
            xy_curve = np.column_stack((x_curve, y_curve))
            #save curve
            curve=(str(base)+'_alloster_i_curve.data')
            np.savetxt(curve,xy_curve,fmt='%.4e')
            c=(c+1)
            e=(c-1)
            draw.write("read xy \""+str(curve)+"\" \n")
            draw.write("s"+str(c)+" symbol 0 \n")
            draw.write("s"+str(c)+" line type 1 \n")
            draw.write("s"+str(c)+" line color 1 \n")
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
    res=(str(base)+'_allosteric_i.res')
    res=open(res,'r')
    tolog=res.read()
    log=open("temp.log",'w')
    log.write(tolog)

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
