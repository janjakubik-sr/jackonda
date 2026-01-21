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

global KD_min, KD_estim, KD_max, Bmax_min, Bmax_estim, Bmax_max

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
        label = wx.StaticText(self, -1, "Saturation - parameter estimates")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer = wx.GridSizer(2, 3, 5, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "KD min:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.KD_min = wx.TextCtrl(self, -1, str(KD_min), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.KD_min, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "KD estimate:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.KD_estim = wx.TextCtrl(self, -1, str(KD_estim), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.KD_estim, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "KD max:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.KD_max = wx.TextCtrl(self, -1, str(KD_max), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.KD_max, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Bmax min:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Bmax_min = wx.TextCtrl(self, -1, str(Bmax_min), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Bmax_min, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Bmax estimate:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Bmax_estim = wx.TextCtrl(self, -1, str(Bmax_estim), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Bmax_estim, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Bmax max:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Bmax_max = wx.TextCtrl(self, -1, str(Bmax_max), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Bmax_max, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
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
x_max_max = 0
y_max_max = 0

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
    if os.path.isfile(str(base)+"_saturation_i_s.res"):
        os.remove(str(base)+"_saturation_i_s.res")
    res = open(str(base)+"_saturation_i_s.res","w")
    res.write("Saturation of single site\n\n")
    res.write("Bmax\t\tKD\t\t\t\tData file\n")
    #prepare file for Grace plot
    if os.path.isfile(str(base)+"_satur_i_s.draw"):
        os.remove(str(base)+"_satur_i_s.draw")
    draw = open(str(base)+"_satur_i_s.draw","w")
    c=-1 #plot counter
    d=0 #symbolcounter
    
    # load data
    x_data = data[:,0]
    y_data = data[:,1]
    y_data_err = data[:,2]
    x_min = np.amin(x_data)
    if np.size(x_data) < 6:
        msg = ('Too few data points in ' +str(selected)+ ' Data will not be analyzed.\n')
        err = err + msg
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    else:
        if x_min < 0:
            msg = ('Negative x value found found! '+str(selected)+'Data will not analyzed\n')
            err = err + msg
            dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            x_max = np.amax(x_data)
            if x_max > x_max_max:
                x_max_max = x_max
            y_max = np.amax(y_data)
            if y_max > y_max_max:
                y_max_max = y_max
            step = x_max / 100
            #get estimates & bounds
            KD_estim = x_max * 0.25
            KD_min = 0
            KD_max = x_max
            Bmax_estim = y_max
            Bmax_min = 0
            Bmax_max = y_max * 2
            dlg = Estimates(None, -1, "Enter values", size=(350, 200),
                           #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                           style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
                           )
            dlg.CenterOnScreen()
            val = dlg.ShowModal()
            if val == wx.ID_OK:
                KD_min = float(dlg.KD_min.GetValue())
                KD_estim = float(dlg.KD_estim.GetValue())
                KD_max = float(dlg.KD_max.GetValue())
                Bmax_min = float(dlg.Bmax_min.GetValue())
                Bmax_estim = float(dlg.Bmax_estim.GetValue())
                Bmax_max = float(dlg.Bmax_max.GetValue())
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
            p0 = np.array([Bmax_estim, KD_estim])
            def func(x, Bmax, KD):
                global KD_min, KD_estim, KD_max, Bmax_min, Bmax_estim, Bmax_max
                KD_min = float(KD_min)
                KD_estim = float(KD_estim)
                KD_max = float(KD_max)
                Bmax_min = float(Bmax_min)
                Bmax_estim = float(Bmax_estim)
                Bmax_max = float(Bmax_max)
                return Bmax*x / (KD + x)
            popt, pcov = opt.curve_fit(func, x_data, y_data, p0, bounds=([Bmax_min,KD_min],[Bmax_max,KD_max]))
            perr = np.sqrt(np.diag(pcov))
            Bmax_calc = (popt[0])
            KD_calc = (popt[1])
            Bmax_err = (perr[0])
            KD_err = (perr[1])
            #write results
            Bmax_res = (str("{0:.2f}".format(Bmax_calc))+' ± '+str("{0:.2f}".format(Bmax_err)))
            KD_res = (str("{0:.2f}".format(KD_calc))+' ± '+str("{0:.2f}".format(KD_err)))
            res.write(str(Bmax_res)+"\t"+str(KD_res)+"\t"+str(selected)+"\n")
            #write Grace plot
            c=(c+1)
            d=(d+1)
            draw.write("read xydy \""+str(selected)+"\" \n")
            draw.write("s"+str(c)+" symbol "+str(d)+" \n")
            draw.write("s"+str(c)+" symbol size 0.8 \n")
            draw.write("s"+str(c)+" symbol color 1 \n")
            draw.write("s"+str(c)+" symbol fill color 0 \n")
            draw.write("s"+str(c)+" symbol fill pattern 1 \n")
            draw.write("s"+str(c)+" errorbar color 1 \n")
            draw.write("s"+str(c)+" errorbar size 0.8 \n")
            draw.write("s"+str(c)+" line type 0 \n")
            draw.write("s"+str(c)+" legend \"K\\sD1\\N="+str("{0:.2f}".format(KD_calc))+' \\#{B1} '+str("{0:.2f}".format(KD_err))+"; B\\sMAX1\\N="+str("{0:.2f}".format(Bmax_calc))+' \\#{B1} '+str("{0:.2f}".format(Bmax_err))+"; "+str(base)+"\" \n")
            #calculate fit
            y_fit = func(x_data, *popt)
            xy_fit = np.column_stack((x_data, y_fit))
            #save fit
            fit=(str(base)+'_satur_i_fit.data')
            np.savetxt(fit,xy_fit,fmt='%.4e')
            #calculate curve
            x_curve = np.arange(0, x_max, step)
            y_curve = func(x_curve, *popt)
            xy_curve = np.column_stack((x_curve, y_curve))
            #save curve
            curve=(str(base)+'_satur_i_curve.data')
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
    res=(str(base)+'_saturation_i_s.res')
    res=open(res,'r')
    tolog=res.read()
    log=open("temp.log",'w')
    log.write(tolog)

    #Plot
    ax_max = x_max_max * 1.1
    ay_max = y_max_max * 1.2
    plt.title("Saturation binding")
    plt.axis([0,ax_max,0,ay_max])
    plt.xlabel("Free")
    plt.ylabel("Bound")
    plt.show()
    #Grace plot
    draw.write("page size 595, 842 \n")
    draw.write("view xmin 0.2 \n")
    draw.write("view xmax 0.8 \n")
    draw.write("view ymin 0.85 \n")
    draw.write("view ymax 1.25 \n")
    draw.write("world xmin 0 \n")
    draw.write("world xmax "+str(ax_max)+" \n")
    draw.write("world ymin 0 \n")
    draw.write("world ymax "+str(ay_max)+" \n")
    draw.write("xaxis label \"Free [ ]\"  \n")
    draw.write("xaxis label font \"Helvetica\"  \n")
    draw.write("xaxis ticklabel font \"Helvetica\"  \n")
    draw.write("xaxis  tick major size 0.8 \n")
    draw.write("xaxis  tick minor size 0.4 \n")
    draw.write("yaxis label \"binding [pmol / mg of protein]\"  \n")
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

