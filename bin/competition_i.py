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

global IC501_min, IC501_estim, IC501_max, IC502_min, IC502_estim, IC502_max, F2_min, F2_estim, F2_max

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
        label = wx.StaticText(self, -1, "Competitive interaction - parameter estimates")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer = wx.GridSizer(3, 3, 5, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "log IC501 min:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.IC501_min = wx.TextCtrl(self, -1, str(IC501_min), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.IC501_min, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "log IC501 estimate:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.IC501_estim = wx.TextCtrl(self, -1, str(IC501_estim), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.IC501_estim, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "log IC501 max:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.IC501_max = wx.TextCtrl(self, -1, str(IC501_max), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.IC501_max, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "log IC502 min:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.IC502_min = wx.TextCtrl(self, -1, str(IC502_min), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.IC502_min, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "log IC502 estimate:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.IC502_estim = wx.TextCtrl(self, -1, str(IC502_estim), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.IC502_estim, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "log IC502 max:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.IC502_max = wx.TextCtrl(self, -1, str(IC502_max), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.IC502_max, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "F2 min:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.F2_min = wx.TextCtrl(self, -1, str(F2_min), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.F2_min, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "F2 estimate:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.F2_estim = wx.TextCtrl(self, -1, str(F2_estim), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.F2_estim, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "F2 max:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.F2_max = wx.TextCtrl(self, -1, str(F2_max), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.F2_max, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
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
    if os.path.isfile(str(base)+"_competition_i.res"):
        os.remove(str(base)+"_competition_i.res")
    res = open(str(base)+"_competition_i.res","w")
    res.write("Competition for two sites\n\n")
    res.write("logIC501\tlogIC502\tF2\t\t\t\tData file\n")
    #prepare file for Grace plot
    if os.path.isfile(str(base)+"_compet_i.draw"):
        os.remove(str(base)+"_compet_i.draw")
    draw = open(str(base)+"_compet_i.draw","w")
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
        msg = ('Too few data points in ' +str(selected)+ ' This data will be skipped\n')
        err = err + msg
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    else:
        if x_min < -15 or x_max > 0:
            msg = ('X value out of range ,<15,0>! '+str(selected)+' will be skipped\n')
            err = err + msg
            dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            if x_max > x_max_max:
                x_max_max = x_max
            if x_min < x_min_min:
                x_min_min = x_min
            step = (x_max - x_min) * 0.01
            #get estimates & bounds
            IC501_estim = x_min + (x_max - x_min) * 0.25
            IC501_min = x_min + 0.5
            IC501_max = x_min + (x_max - x_min) * 0.6
            IC502_estim = x_min + (x_max - x_min) * 0.75
            IC502_min = x_min + (x_max - x_min) * 0.4
            IC502_max = x_max - 0.5
            F2_estim = 50
            F2_min = 1
            F2_max = 99
            dlg = Estimates(None, -1, "Enter values", size=(350, 200),
                           #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                           style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
                           )
            dlg.CenterOnScreen()
            val = dlg.ShowModal()
            if val == wx.ID_OK:
                IC501_min = float(dlg.IC501_min.GetValue())
                IC501_estim = float(dlg.IC501_estim.GetValue())
                IC501_max = float(dlg.IC501_max.GetValue())
                IC502_min = float(dlg.IC502_min.GetValue())
                IC502_estim = float(dlg.IC502_estim.GetValue())
                IC502_max = float(dlg.IC502_max.GetValue())
                F2_min = float(dlg.F2_min.GetValue())
                F2_estim = float(dlg.F2_estim.GetValue())
                F2_max = float(dlg.F2_max.GetValue())
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
            p0 = np.array([IC501_estim, IC502_estim, F2_estim])
            def func(x, IC501, IC502, F2):
                global IC501_min, IC501_estim, IC501_max, IC502_min, IC502_estim, IC502_max, F2_min, F2_estim, F2_max
                IC501_min = float(IC501_min)
                IC501_estim = float(IC501_estim)
                IC501_max = float(IC501_max)
                IC502_min = float(IC502_min)
                IC502_estim = float(IC502_estim)
                IC502_max = float(IC502_max)
                F2_min = float(F2_min)
                F2_estim = float(F2_estim)
                F2_max = float(F2_max)
                return 100 - (100 - F2)*10**x / (10**IC501 + 10**x) - F2*10**x / (10**IC502 + 10**x)
            popt, pcov = opt.curve_fit(func, x_data, y_data, p0, bounds=([IC501_min,IC502_min, F2_min],[IC501_max,IC502_max, F2_max]))
            perr = np.sqrt(np.diag(pcov))
            IC501_calc = (popt[0])
            IC502_calc = (popt[1])
            F2_calc = (popt[2])
            IC501_err = (perr[0])
            IC502_err = (perr[1])
            F2_err = (perr[2])
            #write results
            IC501_res = (str("{0:.2f}".format(IC501_calc))+' ± '+str("{0:.2f}".format(IC501_err)))
            IC502_res = (str("{0:.2f}".format(IC502_calc))+' ± '+str("{0:.2f}".format(IC502_err)))
            F2_res = (str("{0:.2f}".format(F2_calc))+' ± '+str("{0:.2f}".format(F2_err)))
            res.write(str(IC501_res)+"\t"+str(IC502_res)+"\t"+str(F2_res)+"\t\t"+str(selected)+"\n")
            #write Grace plot
            c=(c+1)
            d=(d+1)
            base=os.path.splitext(selected)[0]
            draw.write("read xydy \""+str(selected)+"\" \n")
            draw.write("s"+str(c)+" symbol "+str(d)+" \n")
            draw.write("s"+str(c)+" symbol size 0.8 \n")
            draw.write("s"+str(c)+" symbol color 1 \n")
            draw.write("s"+str(c)+" symbol fill color 0 \n")
            draw.write("s"+str(c)+" symbol fill pattern 1 \n")
            draw.write("s"+str(c)+" errorbar color 1 \n")
            draw.write("s"+str(c)+" errorbar size 0.8 \n")
            draw.write("s"+str(c)+" line type 0 \n")
            draw.write("s"+str(c)+" legend \"log IC\\s501\\N="+str("{0:.2f}".format(IC501_calc))+' \\#{B1} '+str("{0:.2f}".format(IC501_err))+"; log IC\\s502\\N="+str("{0:.2f}".format(IC502_calc))+' \\#{B1} '+str("{0:.2f}".format(IC502_err))+"; F\\s2\\N="+str("{0:.2f}".format(F2_calc))+' \\#{B1} '+str("{0:.2f}".format(F2_err))+";\\n\\n"+str(base)+"\" \n")
            #calculate fit
            y_fit = func(x_data, *popt)
            xy_fit = np.column_stack((x_data, y_fit))
            #save curve
            fit=(str(base)+'_compet_i_fit.data')
            np.savetxt(fit,xy_fit,fmt='%.4e')
            #calculate curve
            x_curve = np.arange(x_min, x_max, step)
            y_curve = func(x_curve, *popt)
            xy_curve = np.column_stack((x_curve, y_curve))
            #save curve
            curve=(str(base)+'_compet_i_curve.data')
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
    res=(str(base)+'_competition_i.res')
    res=open(res,'r')
    tolog=res.read()
    log=open("temp.log",'w')
    log.write(tolog)

    #Plot
    ax_min = x_min_min - 0.5
    ax_max = x_max_max + 0.5
    plt.title("Competition binding")
    plt.axis([ax_min,ax_max,0,120])
    plt.xlabel("ligand [log c]")
    plt.ylabel("tracer bindng [% of control]")
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
    draw.write("world ymax 120 \n")
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
