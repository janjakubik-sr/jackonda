#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Substrate inhibition
Generate five curves varying Ke
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
        label = wx.StaticText(self, -1, "total [E]")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Etot = wx.TextCtrl(self, -1, str(Etot), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Etot, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Agonist logKA")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.pKA = wx.TextCtrl(self, -1, str(pKA), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.pKA, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
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
        label = wx.StaticText(self, -1, "Ke1")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Ke1 = wx.TextCtrl(self, -1, str(Ke1), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Ke1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Ke2")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Ke2 = wx.TextCtrl(self, -1, str(Ke2), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Ke2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Ke3")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Ke3 = wx.TextCtrl(self, -1, str(Ke3), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Ke3, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Ke4")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Ke4 = wx.TextCtrl(self, -1, str(Ke4), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Ke4, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Ke5")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.Ke5 = wx.TextCtrl(self, -1, str(Ke5), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.Ke5, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
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

#simulated parameters
basal = 0
Etot = 1e-6
Rtot = 1e-5
pKA = -7

#define 5 Ke values
Ke1 = 1e-8
Ke2 = 1e-7
Ke3 = 3e-7
Ke4 = 1e-6
Ke5 = 3e-6

#define size of random noise
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
    Etot = float(dlg.Etot.GetValue())
    Rtot = float(dlg.Rtot.GetValue())
    basal = float(dlg.basal.GetValue())
    noise = float(dlg.noise.GetValue())
    pKA = float(dlg.pKA.GetValue())
    Ke1 = float(dlg.Ke1.GetValue())
    Ke2 = float(dlg.Ke2.GetValue())
    Ke3 = float(dlg.Ke3.GetValue())
    Ke4 = float(dlg.Ke4.GetValue())
    Ke5 = float(dlg.Ke5.GetValue())
    log = open("temp.log","w")
    log.write("Modeling OMA of low receptor expression system")
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


#prepare file for writing results
res = open("Model.def","w")
res.write("Operational Model - Depleted system\nVarious agonists\n\n")
res.write("Model parameters\n")
res.write("Etot = "+str(Etot)+"\n")
res.write("Rtot = "+str(Rtot)+"\n")
res.write("logKa = "+str(pKA)+"\n")
res.write("Ke1 = "+str(Ke1)+"\n")
res.write("Ke2 = "+str(Ke2)+"\n")
res.write("Ke3 = "+str(Ke3)+"\n")
res.write("Ke4 = "+str(Ke4)+"\n")
res.write("Ke5 = "+str(Ke5)+"\n")
res.write("noise = "+str(noise)+"\n")
now = time.strftime("%d.%m.%Y %H:%M:%S")
res.write("\n\n"+str(now)+"\n")
res.close()
#binding fuction
def func(x, Rtot, pKA):
    return ((10**x) * Rtot) / ((10**x) + (10**pKA))
x_data = np.linspace((pKA-4),(pKA+4), 17)
y_data = func(x_data, Rtot, pKA)

#response function
def func2(y, Ke):
    return (basal + (Ke + y + Etot - np.sqrt(Ke**2 + 2*Ke*(y+Etot) + (y-Etot)**2))/2/Etot )

#data A
#simulate data
z_data_11 = func2(y_data, Ke1)
z_data_1 = func2(y_data, Ke1) * np.random.normal(size=17, loc=1.0, scale=noise)
z_data_err_1 = np.absolute(np.subtract(z_data_11, z_data_1))
data_gen=np.column_stack((x_data, z_data_1, z_data_err_1))
data=open('Data_A.dat','w')
np.savetxt(data,data_gen,fmt='%.4e')
data.close()
# plot
#get color
i = i + 1
color = (color_list[i])
plt.errorbar(x_data, z_data_1, xerr=None, yerr=z_data_err_1, fmt = color + "o")

#data B
#simulate data
z_data_21 = func2(y_data, Ke2)
z_data_2 = func2(y_data, Ke2) * np.random.normal(size=17, loc=1.0, scale=noise)
z_data_err_2 = np.absolute(np.subtract(z_data_21, z_data_2))
data_gen=np.column_stack((x_data, z_data_2, z_data_err_2))
data=open('Data_B.dat','w')
np.savetxt(data,data_gen,fmt='%.4e')
data.close()
# plot
#get color
i = i + 1
color = (color_list[i])
plt.errorbar(x_data, z_data_2, xerr=None, yerr=z_data_err_2, fmt = color + "o")

#data C
#simulate data
z_data_31 = func2(y_data, Ke3) 
z_data_3 = func2(y_data, Ke3) * np.random.normal(size=17, loc=1.0, scale=noise)
z_data_err_3 = np.absolute(np.subtract(z_data_31, z_data_3))
data_gen=np.column_stack((x_data, z_data_3, z_data_err_3))
data=open('Data_C.dat','w')
np.savetxt(data,data_gen,fmt='%.4e')
data.close()
# plot
#get color
i = i + 1
color = (color_list[i])
plt.errorbar(x_data, z_data_3, xerr=None, yerr=z_data_err_3, fmt = color + "o")

#data D
#simulate data
z_data_41 = func2(y_data, Ke4) 
z_data_4 = func2(y_data, Ke4) * np.random.normal(size=17, loc=1.0, scale=noise)
z_data_err_4 = np.absolute(np.subtract(z_data_41, z_data_4))
data_gen=np.column_stack((x_data, z_data_4, z_data_err_4))
data=open('Data_D.dat','w')
np.savetxt(data,data_gen,fmt='%.4e')
data.close()
# plot
#get color
i = i + 1
color = (color_list[i])
plt.errorbar(x_data, z_data_4, xerr=None, yerr=z_data_err_4, fmt = color + "o")

#data E
#simulate data
z_data_51 = func2(y_data, Ke5) 
z_data_5 = func2(y_data, Ke5) * np.random.normal(size=17, loc=1.0, scale=noise)
z_data_err_5 = np.absolute(np.subtract(z_data_51, z_data_5))
data_gen=np.column_stack((x_data, z_data_5, z_data_5))
data=open('Data_E.dat','w')
np.savetxt(data,data_gen,fmt='%.4e')
data.close()
# plot
#get color
i = i + 1
color = (color_list[i])
plt.errorbar(x_data, z_data_5, xerr=None, yerr=z_data_err_5, fmt = color + "o")

#Show plot
plt.title("Functional response")
plt.xlabel("[A]")
plt.ylabel("Response")
plt.show()
