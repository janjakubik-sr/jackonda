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
        label = wx.StaticText(self, -1, "OMARD - parameter set-up")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer = wx.GridSizer(3, 5, 5, 5)

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
        label = wx.StaticText(self, -1, "")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Agonist logKA")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.logKA = wx.TextCtrl(self, -1, str(logKA), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.logKA, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Agonist logKB")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.logKB = wx.TextCtrl(self, -1, str(logKB), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.logKB, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "tau")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.tau = wx.TextCtrl(self, -1, str(tau), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.tau, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "beta dimer")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.beta = wx.TextCtrl(self, -1, str(beta), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.beta, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "gamma monomer")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.gamma = wx.TextCtrl(self, -1, str(gamma), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.gamma, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "alpha1")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.alpha1 = wx.TextCtrl(self, -1, str(alpha1), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.alpha1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "alpha2")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.alpha2 = wx.TextCtrl(self, -1, str(alpha2), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.alpha2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "alpha3")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.alpha3 = wx.TextCtrl(self, -1, str(alpha3), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.alpha3, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "alpha4")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.alpha4 = wx.TextCtrl(self, -1, str(alpha4), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.alpha4, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "alpha5")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.alpha5 = wx.TextCtrl(self, -1, str(alpha5), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.alpha5, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
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
logKA = -7
logKB = -6
tau = 3
beta = 0.5
gamma = 1

#define four concetrations of B, B1 should be zero
alpha1 = 0.1
alpha2 = 0.3
alpha3 = 1
alpha4 = 3
alpha5 = 10

#define size of random noise
noise = 0.02

#color list
color_list = np.array(['k','b','r','g','c','m','y'])
#initiate color counter
i = -1

dlg = Estimates(None, -1, "Enter values to be simulated", size=(350, 300),
               #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
               style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
               )
dlg.CenterOnScreen()
val = dlg.ShowModal()
if val == wx.ID_OK:
    Emax = float(dlg.Emax.GetValue())
    noise = float(dlg.noise.GetValue())
    logKA = float(dlg.logKA.GetValue())
    logKB = float(dlg.logKB.GetValue())
    tau = float(dlg.tau.GetValue())
    beta = float(dlg.beta.GetValue())
    gamma = float(dlg.gamma.GetValue())    
    alpha1 = float(dlg.alpha1.GetValue())
    alpha2 = float(dlg.alpha2.GetValue())
    alpha3 = float(dlg.alpha3.GetValue())
    alpha4 = float(dlg.alpha4.GetValue())
    alpha5 = float(dlg.alpha5.GetValue())
    log = open("temp.log","w")
    log.write("Modeling OMARD alpha effects")
    log.close()
else:
    msg = ('Modelling was canceled.')
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    log = open("temp.log","w")
    log.write("Error: Data were not simulated")
    log.close()
    tolog = log.read()
    None.__log(tolog)
dlg.Destroy()

x_min = (logKA+logKB)/2 - 4
x_max = (logKA+logKB)/2 + 4
x_data = np.linspace(x_min,x_max,25)

#Save model parameters
res = open("Model.def","w")
res.write("Operational model of agonism at receptor dimers\nEffect of alpha value\n\n")
res.write("Emax = "+str(Emax)+"\n")
res.write("logKA = "+str(logKA)+"\n")
res.write("logKB = "+str(logKB)+"\n")
res.write("tau = "+str(tau)+"\n")
res.write("beta = "+str(beta)+"\n")
res.write("gamma = "+str(gamma)+"\n")
res.write("alpha1 = "+str(alpha1)+"\n")
res.write("alpha2 = "+str(alpha2)+"\n")
res.write("alpha3 = "+str(alpha3)+"\n")
res.write("alpha4 = "+str(alpha4)+"\n")
res.write("alpha5 = "+str(alpha5)+"\n")
now = time.strftime("%d.%m.%Y %H:%M:%S")
res.write("\n\n"+str(now)+"\n")
res.close()

#FR function
def func(x, alpha):
    return ( Emax*(beta*gamma*tau*(10**x)*(alpha*(10**x)+(10**logKA)+(10**logKB))**2)/(beta*gamma*tau*(10**x)*(alpha*(10**x)+(10**logKA)+(10**logKB))**2+(alpha*(10**x)**2+(10**logKA)*(10**logKB)+(10**x)*(10**logKA)+(10**x)*(10**logKB))*(alpha*gamma*(10**x)+beta*gamma*(10**logKB)+beta*(10**logKB))) )

#data A
y_data_11 = func(x_data, alpha1)
y_data_1 = func(x_data, alpha1) * np.random.normal(size=25, loc=1.0, scale=noise)
y_data_err_1 = np.absolute(np.subtract(y_data_11, y_data_1))
data_gen1=np.column_stack((x_data, y_data_1, y_data_err_1))
np.savetxt('Data_A.dat',data_gen1,fmt='%.4e')
#get color
i = i + 1
color = (color_list[i])
#plot
plt.errorbar(x_data, y_data_1, xerr=None, yerr=y_data_err_1, fmt = color + "o")

#data B
y_data_21 = func(x_data, alpha2)
y_data_2 = func(x_data, alpha2) * np.random.normal(size=25, loc=1.0, scale=noise)
y_data_err_2 = np.absolute(np.subtract(y_data_21, y_data_2))
data_gen2=np.column_stack((x_data, y_data_2, y_data_err_2))
np.savetxt('Data_B.dat',data_gen2,fmt='%.4e')
#get color
i = i + 1
color = (color_list[i])
#plot
plt.errorbar(x_data, y_data_2, xerr=None, yerr=y_data_err_2, fmt = color + "o")

#data C
y_data_31 = func(x_data, alpha3)
y_data_3 = func(x_data, alpha3) * np.random.normal(size=25, loc=1.0, scale=noise)
y_data_err_3 = np.absolute(np.subtract(y_data_31, y_data_3))
data_gen3=np.column_stack((x_data, y_data_3, y_data_err_3))
np.savetxt('Data_C.dat',data_gen3,fmt='%.4e')
#get color
i = i + 1
color = (color_list[i])
#plot
plt.errorbar(x_data, y_data_3, xerr=None, yerr=y_data_err_3, fmt = color + "o")

#data D
y_data_41 = func(x_data, alpha4)
y_data_4 = func(x_data, alpha4) * np.random.normal(size=25, loc=1.0, scale=noise)
y_data_err_4 = np.absolute(np.subtract(y_data_41, y_data_4))
data_gen4=np.column_stack((x_data, y_data_4, y_data_err_4))
np.savetxt('Data_D.dat',data_gen4,fmt='%.4e')
#get color
i = i + 1
color = (color_list[i])
#plot
plt.errorbar(x_data, y_data_4, xerr=None, yerr=y_data_err_4, fmt = color + "o")

#data E
y_data_51 = func(x_data, alpha5)
y_data_5 = func(x_data, alpha5) * np.random.normal(size=25, loc=1.0, scale=noise)
y_data_err_5 = np.absolute(np.subtract(y_data_51, y_data_5))
data_gen4=np.column_stack((x_data, y_data_5, y_data_err_5))
np.savetxt('Data_E.dat',data_gen4,fmt='%.4e')
#get color
i = i + 1
color = (color_list[i])
#plot
plt.errorbar(x_data, y_data_5, xerr=None, yerr=y_data_err_5, fmt = color + "o")

#Show plot
plt.title("Functional response of dimers")
plt.xlabel("[A]")
plt.ylabel("Response")
plt.show()
