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


global KD, KA, KB, noise, alpha, beta, gamma, delta, B1, B2, B3, B4

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
        label = wx.StaticText(self, -1, "Allosteric interaction - parameter set-up")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer = wx.GridSizer(3, 4, 5, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Tracer KD")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.KD = wx.TextCtrl(self, -1, str(KD), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.KD, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Modulator A KA")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.KA = wx.TextCtrl(self, -1, str(KA), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.KA, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Modulator B KB")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.KB = wx.TextCtrl(self, -1, str(KB), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.KB, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "noise")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.noise = wx.TextCtrl(self, -1, str(noise), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.noise, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "alpha")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.alpha = wx.TextCtrl(self, -1, str(alpha), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.alpha, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "beta")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.beta = wx.TextCtrl(self, -1, str(beta), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.beta, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "gamma")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.gamma = wx.TextCtrl(self, -1, str(gamma), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.gamma, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "delta")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.delta = wx.TextCtrl(self, -1, str(delta), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.delta, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "[X]")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.CX = wx.TextCtrl(self, -1, str(CX), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.CX, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
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

#error log
if os.path.isfile("Model.def"):
    os.remove("Model.def")

#simulated paraneters
CX = 100e-12
KD = 250e-12
KA = 1e-8
KB = 1e-6
alpha = 0.2
beta = 10
gamma = 10
delta = 1

#define four concetrations of B, B1 should be zero
B1 = 0.000
B2 = 3e-7
B3 = 1e-6
B4 = 3e-6

#define size of random noise
noise = 0.02

dlg = Estimates(None, -1, "Enter values to model", size=(450, 200),
               #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
               style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
               )
dlg.CenterOnScreen()
val = dlg.ShowModal()
if val == wx.ID_OK:
    KD = float(dlg.KD.GetValue())
    KA = float(dlg.KA.GetValue())
    KB = float(dlg.KB.GetValue())
    noise = float(dlg.noise.GetValue())
    alpha = float(dlg.alpha.GetValue())
    beta = float(dlg.beta.GetValue())
    gamma = float(dlg.gamma.GetValue())
    delta = float(dlg.delta.GetValue())
    CX = float(dlg.CX.GetValue())
    B2 = float(dlg.B2.GetValue())
    B3 = float(dlg.B3.GetValue())
    B4 = float(dlg.B4.GetValue())
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
res.write("Allosteric interaction of tracer and 2  allosteric modulators\n\n")
res.write("KD = "+str(KD)+"\n")
res.write("KA = "+str(KA)+"\n")
res.write("KB = "+str(KB)+"\n")
res.write("[X] = "+str(CX)+"\n")
res.write("alpha = "+str(alpha)+"\n")
res.write("beta = "+str(beta)+"\n")
res.write("gamma = "+str(gamma)+"\n")
res.write("delta = "+str(delta)+"\n")
res.write("[B]1 = "+str(B1)+"\n")
res.write("[B]2 = "+str(B2)+"\n")
res.write("[B]3 = "+str(B3)+"\n")
res.write("[B]4 = "+str(B4)+"\n")
now = time.strftime("%d.%m.%Y %H:%M:%S")
res.write("\n\n"+str(now)+"\n")
res.close()


#data A
#define function
def func1(x):
    return 100 * (CX + KD) / (CX + KD * (1 + (10**x) / KA + B1 / KB * (1 + (10**x) / gamma / KA) ) / (1 + (10**x) / alpha / KA + B1 / beta / KB * (1 + (10**x) / alpha / gamma / delta / KA ) ) )
#simulate data
y_data_11 = func1(x_data)
y_data_1 = func1(x_data) * np.random.normal(size=25, loc=1.0, scale=noise)
y_data_err_1 = np.absolute(np.subtract(y_data_11, y_data_1))
data_gen1=np.column_stack((x_data, y_data_1, y_data_err_1))
np.savetxt('Data_A.dat',data_gen1,fmt='%.4e')

#data B
#redefine function
def func2(x):
    return 100 * (CX + KD) / (CX + KD * (1 + (10**x) / KA + B2 / KB * (1 + (10**x) / gamma / KA) ) / (1 + (10**x) / alpha / KA + B2 / beta / KB * (1 + (10**x) / alpha / gamma / delta / KA ) ) )
#simulate data
y_data_21 = func2(x_data)
y_data_2 = func2(x_data) * np.random.normal(size=25, loc=1.0, scale=noise)
y_data_err_2 = np.absolute(np.subtract(y_data_21, y_data_2))
data_gen2=np.column_stack((x_data, y_data_2, y_data_err_2))
np.savetxt('Data_B.dat',data_gen2,fmt='%.4e')


#data C
#redefine function
def func3(x):
    return 100 * (CX + KD) / (CX + KD * (1 + (10**x) / KA + B3 / KB * (1 + (10**x) / gamma / KA) ) / (1 + (10**x) / alpha / KA + B3 / beta / KB * (1 + (10**x) / alpha / gamma / delta / KA ) ) )
#simulate data
y_data_31 = func3(x_data)
y_data_3 = func3(x_data) * np.random.normal(size=25, loc=1.0, scale=noise)
y_data_err_3 = np.absolute(np.subtract(y_data_31, y_data_3))
data_gen3=np.column_stack((x_data, y_data_3, y_data_err_3))
np.savetxt('Data_C.dat',data_gen3,fmt='%.4e')


#data D
#redefine function
def func4(x):
    return 100 * (CX + KD) / (CX + KD * (1 + (10**x) / KA + B4 / KB * (1 + (10**x) / gamma / KA) ) / (1 + (10**x) / alpha / KA + B4 / beta / KB * (1 + (10**x) / alpha / gamma / delta / KA ) ) )
#simulate data
y_data_41 = func4(x_data)
y_data_4 = func4(x_data) * np.random.normal(size=25, loc=1.0, scale=noise)
y_data_err_4 = np.absolute(np.subtract(y_data_41, y_data_4))
data_gen4=np.column_stack((x_data, y_data_4, y_data_err_4))
np.savetxt('Data_D.dat',data_gen4,fmt='%.4e')

