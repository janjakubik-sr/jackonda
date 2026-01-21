#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:35:07 2016

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
#requires
import os
import time
import wx
import numpy as np
import matplotlib.pyplot as plt

global Emax, basal, noise, KA, KB, tauA, tauB, alpha, beta, B1, B2, B3, B4

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
        label = wx.StaticText(self, -1, "OMAMA - parameter set-up")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer = wx.GridSizer(4, 3, 5, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "System Emax")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Emax = wx.TextCtrl(self, -1, str(Emax), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Emax, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "basal")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.basal = wx.TextCtrl(self, -1, str(basal), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.basal, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "noise")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.noise = wx.TextCtrl(self, -1, str(noise), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.noise, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Agonist KA")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.KA = wx.TextCtrl(self, -1, str(KA), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.KA, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Agonist tauA")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.tauA = wx.TextCtrl(self, -1, str(tauA), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.tauA, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "alpha (binding)")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.alpha = wx.TextCtrl(self, -1, str(alpha), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.alpha, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Modulator KB")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.KB = wx.TextCtrl(self, -1, str(KB), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.KB, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Modulator tauB")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.tauB = wx.TextCtrl(self, -1, str(tauB), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.tauB, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "beta (efficacy)")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.beta = wx.TextCtrl(self, -1, str(beta), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.beta, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "[B]2")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.B2 = wx.TextCtrl(self, -1, str(B2), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.B2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "[B]3")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.B3 = wx.TextCtrl(self, -1, str(B3), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.B3, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "[B]4")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.B4 = wx.TextCtrl(self, -1, str(B4), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.B4, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
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
#error log
if os.path.isfile("temp.log"):
    os.remove("temp.log")
err = ''

#error log
if os.path.isfile("Model.def"):
    os.remove("Model.def")
err = ''

#simulated paraneters
Emax = 1
basal = 0
KA = 1e-6
tauA = 3
alpha = 5
KB = 1e-6
tauB = 0.5
beta = 2

#define four concetrations of B, B1 should be zero
B1 = 0.000
B2 = 3e-7
B3 = 1e-6
B4 = 3e-6

#define size of random noise
noise = 0.03

#color list
color_list = np.array(['k','b','r','g','c','m','y'])
#initiate color counter
i = -1

dlg = Estimates(None, -1, "Enter values to model", size=(350, 300),
               #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
               style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
               )
dlg.CenterOnScreen()
val = dlg.ShowModal()
if val == wx.ID_OK:
    Emax = float(dlg.Emax.GetValue())
    noise = float(dlg.noise.GetValue())
    KA = float(dlg.KA.GetValue())
    tauA = float(dlg.tauA.GetValue())
    alpha = float(dlg.alpha.GetValue())
    KB = float(dlg.KB.GetValue())
    tauB = float(dlg.tauB.GetValue())    
    beta = float(dlg.beta.GetValue())
    B2 = float(dlg.B2.GetValue())
    B3 = float(dlg.B3.GetValue())
    B4 = float(dlg.B4.GetValue())
    log = open("temp.log","w")
    log.write("Modeling OMAMA")
    log.close()
    tolog = log.read()
    None.__log(tolog)
else:
    msg = ('Modelling was canceled.')
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    log = open("temp.log","w")
    log.write("Error: Model was not created")
    log.close()
    tolog = log.read()
    None.__log(tolog)
dlg.Destroy()

x_min = np.log10(KA) - 4
x_max = np.log10(KA) + 4
x_data = np.linspace(x_min,x_max,25)

#Save model parameters
res = open("Model.def","w")
res.write("Operational model of allosterically modulated agonism\n\n")
res.write("Emax = "+str(Emax)+"\n")
res.write("KA = "+str(KA)+"\n")
res.write("tauA = "+str(tauA)+"\n")
res.write("alpha = "+str(alpha)+"\n")
res.write("KB = "+str(KB)+"\n")
res.write("tauB = "+str(tauB)+"\n")
res.write("beta = "+str(beta)+"\n")
res.write("[B]1 = "+str(B1)+"\n")
res.write("[B]2 = "+str(B2)+"\n")
res.write("[B]3 = "+str(B3)+"\n")
res.write("[B]4 = "+str(B4)+"\n")
now = time.strftime("%d.%m.%Y %H:%M:%S")
res.write("\n\n"+str(now)+"\n")
res.close()

#define function
def func(x, B):
    return basal + Emax * (tauA * (10**x) * (KB + alpha * beta * B) + tauB * B * KA) / ((10**x) * KB + KA * KB + KA * B + alpha * (10**x) * B + tauA * (10**x) * (KB + alpha * beta  * B) + tauB * B * KA)

#data A
#simulate data
y_data_11 = func(x_data, B1)
y_data_1 = func(x_data, B1) * np.random.normal(size=25, loc=1.0, scale=noise)
y_data_err_1 = np.absolute(np.subtract(y_data_11, y_data_1))
data_gen1=np.column_stack((x_data, y_data_1, y_data_err_1))
np.savetxt('Data_A.dat',data_gen1,fmt='%.4e')
#get color
i = i + 1
color = (color_list[i])
#plot
plt.errorbar(x_data, y_data_1, xerr=None, yerr=y_data_err_1, fmt = color + "o")

#data B
#simulate data
y_data_21 = func(x_data, B2)
y_data_2 = func(x_data, B2) * np.random.normal(size=25, loc=1.0, scale=noise)
y_data_err_2 = np.absolute(np.subtract(y_data_21, y_data_2))
data_gen2=np.column_stack((x_data, y_data_2, y_data_err_2))
np.savetxt('Data_B.dat',data_gen2,fmt='%.4e')
#get color
i = i + 1
color = (color_list[i])
#plot
plt.errorbar(x_data, y_data_2, xerr=None, yerr=y_data_err_2, fmt = color + "o")

#data C
#simulate data
y_data_31 = func(x_data, B3)
y_data_3 = func(x_data, B3) * np.random.normal(size=25, loc=1.0, scale=noise)
y_data_err_3 = np.absolute(np.subtract(y_data_31, y_data_3))
data_gen3=np.column_stack((x_data, y_data_3, y_data_err_3))
np.savetxt('Data_C.dat',data_gen3,fmt='%.4e')
#get color
i = i + 1
color = (color_list[i])
#plot
plt.errorbar(x_data, y_data_3, xerr=None, yerr=y_data_err_3, fmt = color + "o")

#data D
#simulate data
y_data_41 = func(x_data, B4)
y_data_4 = func(x_data, B4) * np.random.normal(size=25, loc=1.0, scale=noise)
y_data_err_4 = np.absolute(np.subtract(y_data_41, y_data_4))
data_gen4=np.column_stack((x_data, y_data_4, y_data_err_4))
np.savetxt('Data_D.dat',data_gen4,fmt='%.4e')
#get color
i = i + 1
color = (color_list[i])
#plot
plt.errorbar(x_data, y_data_4, xerr=None, yerr=y_data_err_4, fmt = color + "o")

#Show plot
plt.title("Functional response")
plt.xlabel("[A]")
plt.ylabel("Response")
plt.show()
