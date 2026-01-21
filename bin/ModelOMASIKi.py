#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Substrate inhibition
Generate five curves varying Ki
"""
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
        label = wx.StaticText(self, -1, "OMA - parameter set-up")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer = wx.GridSizer(2, 5, 5, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "total [R]")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Rtot = wx.TextCtrl(self, -1, str(Rtot), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Rtot, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Emax")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Emax = wx.TextCtrl(self, -1, str(Emax), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Emax, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Agonist logKA")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.pKA = wx.TextCtrl(self, -1, str(pKA), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.pKA, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Ke")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Ke = wx.TextCtrl(self, -1, str(Ke), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Ke, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "noise")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.noise = wx.TextCtrl(self, -1, str(noise), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.noise, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)
        
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Ki1")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Ki1 = wx.TextCtrl(self, -1, str(Ki1), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Ki1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Ki2")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Ki2 = wx.TextCtrl(self, -1, str(Ki2), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Ki2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Ki3")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Ki3 = wx.TextCtrl(self, -1, str(Ki3), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Ki3, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Ki4")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Ki4 = wx.TextCtrl(self, -1, str(Ki4), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Ki4, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Ki5")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Ki5 = wx.TextCtrl(self, -1, str(Ki5), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Ki5, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
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

#parameters
#Ki
Ki1 = 0.1
Ki2 = 0.5
Ki3 = 1
Ki4 = 2
Ki5 = 10
#constant parameters
Emax =  1
Rtot = 1
Ke = 3.333
pKA = -6
noise = 0.02

#color list
color_list = np.array(['k','b','r','g','c','m','y'])
#initiate color counter
i = -1

dlg = Estimates(None, -1, "Enter values to be simulated", size=(350, 250),
               #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
               style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
               )
dlg.CenterOnScreen()
val = dlg.ShowModal()
if val == wx.ID_OK:
    Emax = float(dlg.Emax.GetValue())
    Rtot = float(dlg.Rtot.GetValue())
    Ke = float(dlg.Ke.GetValue())
    noise = float(dlg.noise.GetValue())
    pKA = float(dlg.pKA.GetValue())
    Ki1 = float(dlg.Ki1.GetValue())
    Ki2 = float(dlg.Ki2.GetValue())
    Ki3 = float(dlg.Ki3.GetValue())
    Ki4 = float(dlg.Ki4.GetValue())
    Ki5 = float(dlg.Ki5.GetValue())
    log = open("temp.log","w")
    log.write("Modeling OMA of substrate inhibition")
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

#prepare file for writing parameters
res = open("Model.def","w")
res.write("Operational Model - Substrate inhibition\n\n")
res.write("Model parameters\n")
res.write("Emax = "+str(Emax)+"\n")
res.write("Rtot = "+str(Rtot)+"\n")
res.write("Ke = "+str(Ke)+"\n")
res.write("logKa = "+str(pKA)+"\n")
res.write("Ki1 = "+str(Ki1)+"\n")
res.write("Ki2 = "+str(Ki2)+"\n")
res.write("Ki3 = "+str(Ki3)+"\n")
res.write("Ki4 = "+str(Ki4)+"\n")
res.write("Ki5 = "+str(Ki5)+"\n")
res.write("noise = "+str(noise)+"\n")
now = time.strftime("%d.%m.%Y %H:%M:%S")
res.write("\n\n"+str(now)+"\n")
res.close()

#x_data
x_data = np.linspace((pKA-4),(pKA+4), 25)

#binding fuction
def func(x):
    return ((10**x) * Rtot) / ((10**x) + (10**pKA))

#y_data
y_data = func(x_data)

#response function
def ffunc(y, Ki):
    return ( Emax * y / (Ke + y * (1 + y / Ki )) )

#data A
#simulate data
z_data_11 = ffunc(y_data, Ki1) 
z_data_1 = ffunc(y_data, Ki1) * np.random.normal(size=25, loc=1.0, scale=noise)
z_data_err_1 = np.absolute(np.subtract(z_data_11, z_data_1))
data_gen=np.column_stack((x_data, z_data_1, z_data_err_1))
data=open('Data_A.dat','w')
np.savetxt(data,data_gen,fmt='%.4e')
data.close()
#get color
i = i + 1
color = (color_list[i])
#plot
plt.errorbar(x_data, z_data_1, xerr=None, yerr=z_data_err_1, fmt = color + "o")

#data B
#simulate data
z_data_21 = ffunc(y_data, Ki2) 
z_data_2 = ffunc(y_data, Ki2) * np.random.normal(size=25, loc=1.0, scale=noise)
z_data_err_2 = np.absolute(np.subtract(z_data_21, z_data_2))
data_gen=np.column_stack((x_data, z_data_2, z_data_err_2))
data=open('Data_B.dat','w')
np.savetxt(data,data_gen,fmt='%.4e')
data.close()
#get color
i = i + 1
color = (color_list[i])
#plot
plt.errorbar(x_data, z_data_2, xerr=None, yerr=z_data_err_2, fmt = color + "o")

#data C
#simulate data
z_data_31 = ffunc(y_data, Ki3) 
z_data_3 = ffunc(y_data, Ki3) * np.random.normal(size=25, loc=1.0, scale=noise)
z_data_err_3 = np.absolute(np.subtract(z_data_31, z_data_3))
data_gen=np.column_stack((x_data, z_data_3, z_data_err_3))
data=open('Data_C.dat','w')
np.savetxt(data,data_gen,fmt='%.4e')
data.close()
#get color
i = i + 1
color = (color_list[i])
#plot
plt.errorbar(x_data, z_data_3, xerr=None, yerr=z_data_err_3, fmt = color + "o")

#data D
#simulate data
z_data_41 = ffunc(y_data, Ki4) 
z_data_4 = ffunc(y_data, Ki4) * np.random.normal(size=25, loc=1.0, scale=noise)
z_data_err_4 = np.absolute(np.subtract(z_data_41, z_data_4))
data_gen=np.column_stack((x_data, z_data_4, z_data_err_4))
data=open('Data_D.dat','w')
np.savetxt(data,data_gen,fmt='%.4e')
data.close()
#get color
i = i + 1
color = (color_list[i])
#plot
plt.errorbar(x_data, z_data_4, xerr=None, yerr=z_data_err_4, fmt = color + "o")

#data E
#simulate data
z_data_51 = ffunc(y_data, Ki5) 
z_data_5 = ffunc(y_data, Ki5) * np.random.normal(size=25, loc=1.0, scale=noise)
z_data_err_5 = np.absolute(np.subtract(z_data_51, z_data_5))
data_gen=np.column_stack((x_data, z_data_5, z_data_5))
data=open('Data_E.dat','w')
np.savetxt(data,data_gen,fmt='%.4e')
data.close()
#get color
i = i + 1
color = (color_list[i])
#plot
plt.errorbar(x_data, z_data_5, xerr=None, yerr=z_data_err_5, fmt = color + "o")

#Show plot
plt.title("Non-competitive autoinhibition")
plt.xlabel("[A]")
plt.ylabel("Response")
plt.show()
