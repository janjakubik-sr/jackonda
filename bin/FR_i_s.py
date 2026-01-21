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

global EC50_min, EC50_estim, EC50_max, Emax_min, Emax_estim, Emax_max, nH_min, nH_estim, nH_max

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
        label = wx.StaticText(self, -1, "Functional response - parameter estimates")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer = wx.GridSizer(3, 3, 5, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "EC50 min:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.EC50_min = wx.TextCtrl(self, -1, str(EC50_min), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.EC50_min, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "EC50 estimate:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.EC50_estim = wx.TextCtrl(self, -1, str(EC50_estim), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.EC50_estim, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "EC50 max:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.EC50_max = wx.TextCtrl(self, -1, str(EC50_max), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.EC50_max, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Emax min:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Emax_min = wx.TextCtrl(self, -1, str(Emax_min), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Emax_min, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Emax estimate:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Emax_estim = wx.TextCtrl(self, -1, str(Emax_estim), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Emax_estim, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Emax max:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Emax_max = wx.TextCtrl(self, -1, str(Emax_max), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Emax_max, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "nH min:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.nH_min = wx.TextCtrl(self, -1, str(nH_min), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.nH_min, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "nH estimate:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.nH_estim = wx.TextCtrl(self, -1, str(nH_estim), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.nH_estim, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "nH max:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.nH_max = wx.TextCtrl(self, -1, str(nH_max), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.nH_max, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
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
y_max_max = 1

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
    if os.path.isfile(str(base)+"_FR_i_s.res"):
        os.remove(str(base)+"_FR_i_s.res")
    res = open(str(base)+"_FR_i_s.res","w")
    res.write("Functional response\n\n")
    res.write("Emax\tlogEC50\t\tEmax2\tlogEC502\t\t\t\tData file\n")
    #prepare file for Grace plot
    if os.path.isfile(str(base)+"_FR_i_s.draw"):
        os.remove(str(base)+"_FR_i_s.draw")
    draw = open(str(base)+"_FR_i_s.draw","w")
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
            if y_max > y_max_max:
                y_max_max = y_max
            step = (x_max - x_min) * 0.01
            #get estimates & bounds
            EC50_estim = x_min + (x_max - x_min) * 0.5
            EC50_min = x_min + 0.5
            EC50_max = x_max - 0.5
            nH_estim = 1
            nH_min = 0.5
            nH_max = 2
            if (y_max - 1) > ( 1 - y_min):
                Emax_estim = y_max
                Emax_min = 1 + (y_max -1) * 0.5
                Emax_max = 1 + (y_max -1) * 2
            else:
                Emax_estim = 0.5
                Emax_min = 0
                Emax_max = 1
            dlg = Estimates(None, -1, "Enter values", size=(350, 200),
                           #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                           style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
                           )
            dlg.CenterOnScreen()
            val = dlg.ShowModal()
            if val == wx.ID_OK:
                EC50_min = float(dlg.EC50_min.GetValue())
                EC50_estim = float(dlg.EC50_estim.GetValue())
                EC50_max = float(dlg.EC50_max.GetValue())
                Emax_min = float(dlg.Emax_min.GetValue())
                Emax_estim = float(dlg.Emax_estim.GetValue())
                Emax_max = float(dlg.Emax_max.GetValue())
                nH_min = float(dlg.nH_min.GetValue())
                nH_estim = float(dlg.nH_estim.GetValue())
                nH_max = float(dlg.nH_max.GetValue())
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
            p0 = np.array([Emax_estim, EC50_estim, nH_estim])
            def func(x, Emax, EC50, nH):
                global EC50_min, EC50_estim, EC50_max, Emax_min, Emax_estim, Emax_max, nH_min, nH_estim, nH_max
                EC50_min = float(EC50_min)
                EC50_estim = float(EC50_estim)
                EC50_max = float(EC50_max)
                Emax_min = float(Emax_min)
                Emax_estim = float(Emax_estim)
                Emax_max = float(Emax_max)
                nH_min = float(nH_min)
                nH_estim = float(nH_estim)
                nH_max = float(nH_max)
                return 1 + (Emax -1) / (1 + 10**((EC50-x)*nH))
            popt, pcov = opt.curve_fit(func, x_data, y_data, p0, bounds=([Emax_min, EC50_min, nH_min],[Emax_max, EC50_max, nH_max]))
            perr = np.sqrt(np.diag(pcov))
            Emax_calc = (popt[0])
            EC50_calc = (popt[1])
            nH_calc = (popt[2])
            Emax_err = (perr[0])
            EC50_err = (perr[1])
            nH_err = (perr[2])
            #write results
            Emax_res = (str("{0:.2f}".format(Emax_calc))+' ± '+str("{0:.2f}".format(Emax_err)))
            EC50_res = (str("{0:.2f}".format(EC50_calc))+' ± '+str("{0:.2f}".format(EC50_err)))
            nH_res = (str("{0:.2f}".format(nH_calc))+' ± '+str("{0:.2f}".format(nH_err)))
            res.write(str(Emax_res)+"\t"+str(EC50_res)+"\t\t"+str(nH_res)+"\t"+str(selected)+"\n")
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
            draw.write("s"+str(c)+" legend \"log EC\\s50\\N="+str("{0:.2f}".format(EC50_calc))+' \\#{B1} '+str("{0:.2f}".format(EC50_err))+"; E\\sMAX\\N="+str("{0:.2f}".format(Emax_calc))+' \\#{B1} '+str("{0:.2f}".format(Emax_err))+"; n\\sH\\N="+str("{0:.2f}".format(nH_calc))+' \\#{B1} '+str("{0:.2f}".format(nH_err))+";\n"+str(base)+"\" \n")
            #calculate fit
            y_fit = func(x_data, *popt)
            xy_fit = np.column_stack((x_data, y_fit))
            #save fit
            fit=(str(base)+'_FR_i_s_fit.data')
            np.savetxt(fit,xy_fit,fmt='%.4e')
            #calculate curve
            x_curve = np.arange(x_min, x_max, step)
            y_curve = func(x_curve, *popt)
            xy_curve = np.column_stack((x_curve, y_curve))
            #save curve
            curve=(str(base)+'_FR_i_s_curve.data')
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
    res=(str(base)+'_FR_i_s.res')
    res=open(res,'r')
    tolog=res.read()
    log=open("temp.log",'w')
    log.write(tolog)

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
log.write(err)
log.close()

