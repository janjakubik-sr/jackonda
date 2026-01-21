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

global Emax, KA, basal, noise, tau1, tau2, tau3, tau4, tau5

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
        label = wx.StaticText(self, -1, "OMA - parameter set-up")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer = wx.GridSizer(2, 5, 5, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "System Emax")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Emax = wx.TextCtrl(self, -1, str(Emax), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Emax, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "KA")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.KA = wx.TextCtrl(self, -1, str(KA), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.KA, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "basal")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.basal = wx.TextCtrl(self, -1, str(basal), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.basal, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "noise")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.noise = wx.TextCtrl(self, -1, str(noise), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.noise, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "tau1")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.tau1 = wx.TextCtrl(self, -1, str(tau1), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.tau1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "tau2")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.tau2 = wx.TextCtrl(self, -1, str(tau2), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.tau2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "tau3")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.tau3 = wx.TextCtrl(self, -1, str(tau3), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.tau3, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "tau4")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.tau4 = wx.TextCtrl(self, -1, str(tau4), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.tau4, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "tau5")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.tau5 = wx.TextCtrl(self, -1, str(tau5), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.tau5, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

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
tau1 = 0.1
tau2 = 1
tau3 = 10
tau4 = 100
tau5 = 1000

#define size of random noise
noise = 0.03

#color list
color_list = np.array(['k','b','r','g','c','m','y'])
#initiate color counter
i = -1

dlg = Estimates(None, -1, "Enter values to model", size=(150, 500),
               #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
               style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
               )
dlg.CenterOnScreen()
val = dlg.ShowModal()
if val == wx.ID_OK:
    Emax = float(dlg.Emax.GetValue())
    basal = float(dlg.basal.GetValue())
    noise = float(dlg.noise.GetValue())
    KA = float(dlg.KA.GetValue())
    tau1 = float(dlg.tau1.GetValue())
    tau2 = float(dlg.tau2.GetValue())
    tau3 = float(dlg.tau3.GetValue())
    tau4 = float(dlg.tau4.GetValue())
    tau5 = float(dlg.tau5.GetValue())
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
res.write("Operational model of agonism\n\n")
res.write("Emax = "+str(Emax)+"\n")
res.write("basal = "+str(basal)+"\n")
res.write("KA = "+str(KA)+"\n")
res.write("tau1 = "+str(tau1)+"\n")
res.write("tau2 = "+str(tau2)+"\n")
res.write("tau3 = "+str(tau3)+"\n")
res.write("tau4 = "+str(tau4)+"\n")
res.write("tau5 = "+str(tau5)+"\n")
now = time.strftime("%d.%m.%Y %H:%M:%S")
res.write("\n\n"+str(now)+"\n")
res.close()


#data A
#define function
def func(x, tau):
    return ( basal+((10**x) * tau1 * Emax) / ((10**x) * (1 + tau) + KA))
#simulate data
y_data_11 = func(x_data, tau1)
y_data_1 = func(x_data, tau1) * np.random.normal(size=25, loc=1.0, scale=noise)
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
y_data_21 = func(x_data, tau2)
y_data_2 = func(x_data, tau2) * np.random.normal(size=25, loc=1.0, scale=noise)
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
y_data_31 = func(x_data, tau3)
y_data_3 = func(x_data, tau3) * np.random.normal(size=25, loc=1.0, scale=noise)
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
y_data_41 = func(x_data, tau4)
y_data_4 = func(x_data, tau4) * np.random.normal(size=25, loc=1.0, scale=noise)
y_data_err_4 = np.absolute(np.subtract(y_data_41, y_data_4))
data_gen4=np.column_stack((x_data, y_data_4, y_data_err_4))
np.savetxt('Data_D.dat',data_gen4,fmt='%.4e')
#get color
i = i + 1
color = (color_list[i])
#plot
plt.errorbar(x_data, y_data_4, xerr=None, yerr=y_data_err_4, fmt = color + "o")

#data E
#simulate data
y_data_51 = func(x_data, tau5)
y_data_5 = func(x_data, tau5) * np.random.normal(size=25, loc=1.0, scale=noise)
y_data_err_5 = np.absolute(np.subtract(y_data_51, y_data_5))
data_gen5=np.column_stack((x_data, y_data_5, y_data_err_5))
np.savetxt('Data_E.dat',data_gen5,fmt='%.4e')
#get color
i = i + 1
color = (color_list[i])
#plot
plt.errorbar(x_data, y_data_5, xerr=None, yerr=y_data_err_5, fmt = color + "o")

#Show plot
plt.title("Functional response")
plt.xlabel("[A]")
plt.ylabel("Response")
plt.show()
