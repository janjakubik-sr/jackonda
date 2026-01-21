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
import scipy.optimize as opt

#color list
color_list = np.array(['k','b','r','g','c','m','y'])
#initiate color couter
i = -1

#temp log
if os.path.isfile("temp.log"):
    os.remove("temp.log")
log = open("temp.log","w")

#results log
if os.path.isfile("FR_OMDI_3D.res"):
    os.remove("FR_OMDI_3D.res")
res = open("FR_OMDI_3D.res","w")

#prepare file for Grace plot
if os.path.isfile("FR_OMDI_3D.draw"):
    os.remove("FR_OMDI_3D.draw")
draw = open("FR_OMDI_3D.draw","w")
c=-1 #plot counter
d=0 #symbolcounter


global Emax, basal, KA, tauA, tauB, B1, B2, B3, B4, B5

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
        label = wx.StaticText(self, -1, "OMDI - parameter set-up: 6 curves including control.")
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
        label = wx.StaticText(self, -1, "")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
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
        label = wx.StaticText(self, -1, "")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "[B]0 = 0")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "[B]1")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.B1 = wx.TextCtrl(self, -1, str(B1), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.B1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
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

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "[B]5")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.B5 = wx.TextCtrl(self, -1, str(B5), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.B5, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
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

#suggested paraneters
Emax = 1
basal = 0
KA = 1e-6
tauA = 3



#define four concetrations of B, B0 should be zero
B0 = 0.000
B1 = 1e-7
B2 = 3e-7
B3 = 1e-6
B4 = 3e-6
B5 = 1e-5

#set estimates and bounds
KB_ini = 1e-6
KB_min = 1e-9
KB_max = 1e-3
KC_ini = 1e-6
KC_min = 1e-9
KC_max = 1e-3
alpha_ini = 2
alpha_min = 0.01
alpha_max = 100
beta_ini = 10
beta_min =0.01
beta_max = 100
gamma_ini = 3
gamma_min = 0.01
gamma_max = 100

dlg = Estimates(None, -1, "Enter system parameters for 6 curves including control.", size=(350, 300),
               #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
               style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
               )
dlg.CenterOnScreen()
val = dlg.ShowModal()
if val == wx.ID_OK:
    basal = float(dlg.basal.GetValue())
    Emax = float(dlg.Emax.GetValue())
    KA = float(dlg.KA.GetValue())
    tauA = float(dlg.tauA.GetValue())
    B1 = float(dlg.B1.GetValue())
    B2 = float(dlg.B2.GetValue())    
    B3 = float(dlg.B3.GetValue())
    B4 = float(dlg.B4.GetValue())
    B5 = float(dlg.B5.GetValue())
else:
    msg = ("Fitting was canceled.")
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    log.write("Error: Fitting was canceled")
    tolog = log.read()
    None.__log(tolog)

#select files
dialog = wx.FileDialog(None, "Choose a control curve, [B] = "+str(B0)+"\n", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected_0=dialog.GetPath()
    data_0 = np.loadtxt(selected_0)    
else:
    msg = ("Fitting was canceled.")
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    log.write("Error: Fitting was canceled")
    tolog = log.read()
    None.__log(tolog)

dialog = wx.FileDialog(None, "Choose a curve with the concentration, [B] = "+str(B1)+"\n", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected_1=dialog.GetPath()
    data_1 = np.loadtxt(selected_1)    
else:
    msg = ("Fitting was canceled.")
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    log.write("Error: Fitting was canceled")
    tolog = log.read()
    None.__log(tolog)

dialog = wx.FileDialog(None, "Choose a curve with the concentration, [B] = "+str(B2)+"\n", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected_2=dialog.GetPath()
    data_2 = np.loadtxt(selected_2)    
else:
    msg = ("Fitting was canceled.")
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    log.write("Error: Fitting was canceled")
    tolog = log.read()
    None.__log(tolog)

dialog = wx.FileDialog(None, "Choose a curve with the concentration, [B] = "+str(B3)+"\n", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected_3=dialog.GetPath()
    data_3 = np.loadtxt(selected_3)    
else:
    msg = ("Fitting was canceled.")
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    log.write("Error: Fitting was canceled")
    tolog = log.read()
    None.__log(tolog)

dialog = wx.FileDialog(None, "Choose a curve with the concentration, [B] = "+str(B4)+"\n", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected_4=dialog.GetPath()
    data_4 = np.loadtxt(selected_4)    
else:
    msg = ("Fitting was canceled.")
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    log.write("Error: Fitting was canceled")
    tolog = log.read()
    None.__log(tolog)

dialog = wx.FileDialog(None, "Choose a curve with the concentration, [B] = "+str(B5)+"\n", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected_5=dialog.GetPath()
    data_5 = np.loadtxt(selected_5)    
else:
    msg = ("Fitting was canceled.")
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    log.write("Error: Fitting was canceled")
    tolog = log.read()
    None.__log(tolog)

#load data
data_0 = np.loadtxt(selected_0)
data_1 = np.loadtxt(selected_1)
data_2 = np.loadtxt(selected_2)
data_3 = np.loadtxt(selected_3)
data_4 = np.loadtxt(selected_4)
data_5 = np.loadtxt(selected_5)

#create 3D data set
data_x_0 = data_0[:,0]
data_y_0 = np.linspace(B1,B1,len(data_0))
data_z_0 = data_0[:,1]
data_zerr_0 = data_0[:,2]
data_x_1 = data_1[:,0]
data_y_1 = np.linspace(B1,B1,len(data_1))
data_z_1 = data_1[:,1]
data_zerr_1 = data_1[:,2]
data_x_2 = data_2[:,0]
data_y_2 = np.linspace(B2,B2,len(data_2))
data_z_2 = data_2[:,1]
data_zerr_2 = data_2[:,2]
data_x_3 = data_3[:,0]
data_y_3 = np.linspace(B3,B3,len(data_3))
data_z_3 = data_3[:,1]
data_zerr_3 = data_3[:,2]
data_x_4 = data_4[:,0]
data_y_4 = np.linspace(B4,B4,len(data_4))
data_z_4 = data_4[:,1]
data_zerr_4 = data_4[:,2]
data_x_5 = data_5[:,0]
data_y_5 = np.linspace(B5,B5,len(data_5))
data_z_5 = data_5[:,1]
data_zerr_5 = data_5[:,2]
x_data = np.concatenate((data_x_0,data_x_1,data_x_2,data_x_3,data_x_4,data_x_5),axis=None)
y_data = np.concatenate((data_y_0,data_y_1,data_y_2,data_y_3,data_y_4,data_y_5),axis=None)
z_data = np.concatenate((data_z_0,data_z_1,data_z_2,data_z_3,data_z_4,data_z_5),axis=None)
z_data_err = np.concatenate((data_zerr_0,data_zerr_1,data_zerr_2,data_zerr_3,data_zerr_4,data_zerr_5),axis=None)

#compute KE
KE = 1/tauA
#fit data
p1 = [KB_ini, KC_ini, alpha_ini, beta_ini, gamma_ini]
#Define global fit function
def func_glob(x, y, p):
    KB, KC, alpha, beta, gamma = p
    return basal + Emax * (( KB*KC*(10**x) / (KA*KB*KC+KB*KC*(10**x)+KA*KC*y+alpha*KC*(10**x)*y+KA*KB*y+beta*KA*(10**x)*y) )/KE+gamma*( alpha*KC*(10**x)*y / (KA*KB*KC+KB*KC*(10**x)+KA*KC*y+alpha*KC*(10**x)*y+KA*KB*y+beta*KA*(10**x)*y) )/KE)/(( KB*KC*(10**x) / (KA*KB*KC+KB*KC*(10**x)+KA*KC*y+alpha*KC*(10**x)*y+KA*KB*y+beta*KA*(10**x)*y) )/KE+gamma*( alpha*KC*(10**x)*y / (KA*KB*KC+KB*KC*(10**x)*KA*KC*y+alpha*KC*(10**x)*y+KA*KB*y+beta*KA*(10**x)*y) )/KE+1)
def err(p, x, y, z):
    return func_glob(x, y, p) - z
pg_estim = p1
pg_opt, cov_x, infodict, errmsg, success = opt.leastsq(err, pg_estim, args=(x_data, y_data, z_data), full_output=1, epsfcn=0.0001)
residuals = err(pg_opt, x_data, y_data, z_data)
reduced_chi_square = np.sum(residuals**2)/(len(x_data)-3)
pg_cov = cov_x * reduced_chi_square
pg_err = np.sqrt(np.diag(pg_cov))
KB_calc = (pg_opt[0])
KB_err = (pg_err[0])
KC_calc = (pg_opt[1])
KC_err = (pg_err[1])
alpha_calc = (pg_opt[2])
alpha_err = (pg_err[2])
beta_calc = (pg_opt[3])
beta_err = (pg_err[3])
gamma_calc = (pg_opt[4])
gamma_err = (pg_err[4])
KB_res = (str("{0:.4g}".format(KB_calc))+" ± "+str("{0:.4g}".format(KB_err)))
KC_res = (str("{0:.4g}".format(KC_calc))+" ± "+str("{0:.4g}".format(KC_err)))
alpha_res = (str("{0:.4g}".format(alpha_calc))+" ± "+str("{0:.4g}".format(alpha_err)))
beta_res = (str("{0:.4g}".format(beta_calc))+" ± "+str("{0:.4g}".format(beta_err)))
gamma_res = (str("{0:.4g}".format(gamma_calc))+" ± "+str("{0:.4g}".format(gamma_err)))

#prepare file for writing results
res.write("OMDI 3D-fit\n\n")
res.write("KA = "+str(KA)+"\ntauA = "+str(tauA)+"\nB0 = 0\nB1 = "+str(B1)+"\nB2 = "+str(B2)+"\nB3 = "+str(B3)+"\nB4 = "+str(B4)+"\nB5 = "+str(B5)+"\n\n")
res.write("3D fit\n")
res.write("KB = "+str(KB_res)+"\nKC = "+str(KC_res)+"\n")
res.write("alpha = "+str(alpha_res)+"\nbeta = "+str(beta_res)+"\ngamma = "+str(gamma_res)+"\n")

#calculate curve 0
x_calc_0 = np.linspace(np.amin(data_x_0),np.amax(data_x_1),100)
y_calc_0 = np.linspace(B0,B0,100)
z_calc_0 = func_glob(x_calc_0, y_calc_0, pg_opt)
xz_calc_0 = np.column_stack((x_calc_0, z_calc_0))
np.savetxt('Data_0_OMDI_3D.fit.data',xz_calc_0,fmt='%.4e')
#get color
i = i + 1
color = (color_list[i])
# plot set 0
plt.plot(x_calc_0, z_calc_0, color)
plt.errorbar(data_x_0, data_z_0, xerr=None, yerr=data_zerr_0, fmt = color + "o")
#write Grace plot 0
c=(c+1)
d=(d+1)
draw.write("read xydy \""+str(selected_0)+"\" \n")
draw.write("s"+str(c)+" symbol "+str(d)+" \n")
draw.write("s"+str(c)+" symbol size 0.8 \n")
draw.write("s"+str(c)+" symbol color "+str(d)+" \n")
draw.write("s"+str(c)+" symbol fill color "+str(d)+" \n")
draw.write("s"+str(c)+" symbol fill pattern 1 \n")
draw.write("s"+str(c)+" errorbar color "+str(d)+" \n")
draw.write("s"+str(c)+" errorbar size 0.8 \n")
draw.write("s"+str(c)+" line type 0 \n")
c=(c+1)
e=(c-1)
fit=('Data_0_OMDI_3D.fit.data')
draw.write("read xy \""+str(fit)+"\" \n")
draw.write("s"+str(c)+" symbol 0 \n")
draw.write("s"+str(c)+" line type 1 \n")
draw.write("s"+str(c)+" line color "+str(d)+" \n")
draw.write("s"+str(c)+" layer 51 \n")
draw.write("s"+str(c)+" legend off \n")


#calculate curve 1
x_calc_1 = np.linspace(np.amin(data_x_1),np.amax(data_x_1),100)
y_calc_1 = np.linspace(B1,B1,100)
z_calc_1 = func_glob(x_calc_1, y_calc_1, pg_opt)
xz_calc_1 = np.column_stack((x_calc_1, z_calc_1))
np.savetxt('Data_1_OMDI_3D.fit.data',xz_calc_1,fmt='%.4e')
#get color
i = i + 1
color = (color_list[i])
# plot set 1
plt.plot(x_calc_1, z_calc_1, color)
plt.errorbar(data_x_1, data_z_1, xerr=None, yerr=data_zerr_1, fmt = color + "o")
#write Grace plot 1
c=(c+1)
d=(d+1)
draw.write("read xydy \""+str(selected_1)+"\" \n")
draw.write("s"+str(c)+" symbol "+str(d)+" \n")
draw.write("s"+str(c)+" symbol size 0.8 \n")
draw.write("s"+str(c)+" symbol color "+str(d)+" \n")
draw.write("s"+str(c)+" symbol fill color "+str(d)+" \n")
draw.write("s"+str(c)+" symbol fill pattern 1 \n")
draw.write("s"+str(c)+" errorbar color "+str(d)+" \n")
draw.write("s"+str(c)+" errorbar size 0.8 \n")
draw.write("s"+str(c)+" line type 0 \n")
c=(c+1)
e=(c-1)
fit=('Data_1_OMDI_3D.fit.data')
draw.write("read xy \""+str(fit)+"\" \n")
draw.write("s"+str(c)+" symbol 0 \n")
draw.write("s"+str(c)+" line type 1 \n")
draw.write("s"+str(c)+" line color "+str(d)+" \n")
draw.write("s"+str(c)+" layer 51 \n")
draw.write("s"+str(c)+" legend off \n")

#calculate curve 2
x_calc_2 = np.linspace(np.amin(data_x_2),np.amax(data_x_2),100)
y_calc_2 = np.linspace(B2,B2,100)
z_calc_2 = func_glob(x_calc_2, y_calc_2, pg_opt)
xz_calc_2 = np.column_stack((x_calc_2, z_calc_2))
np.savetxt('Data_2_OMDI_3D.fit.data',xz_calc_2,fmt='%.4e')
#get color
i = i + 1
color = (color_list[i])
# plot set 2
plt.plot(x_calc_2, z_calc_2, color)
plt.errorbar(data_x_2, data_z_2, xerr=None, yerr=data_zerr_2, fmt = color + "o")
#write Grace plot 2
c=(c+1)
d=(d+1)
draw.write("read xydy \""+str(selected_2)+"\" \n")
draw.write("s"+str(c)+" symbol "+str(d)+" \n")
draw.write("s"+str(c)+" symbol size 0.8 \n")
draw.write("s"+str(c)+" symbol color "+str(d)+" \n")
draw.write("s"+str(c)+" symbol fill color "+str(d)+" \n")
draw.write("s"+str(c)+" symbol fill pattern 1 \n")
draw.write("s"+str(c)+" errorbar color "+str(d)+" \n")
draw.write("s"+str(c)+" errorbar size 0.8 \n")
draw.write("s"+str(c)+" line type 0 \n")
c=(c+1)
e=(c-1)
fit=('Data_2_OMDI_3D.fit.data')
draw.write("read xy \""+str(fit)+"\" \n")
draw.write("s"+str(c)+" symbol 0 \n")
draw.write("s"+str(c)+" line type 1 \n")
draw.write("s"+str(c)+" line color "+str(d)+" \n")
draw.write("s"+str(c)+" layer 51 \n")
draw.write("s"+str(c)+" legend off \n")

#calculate curve 3
x_calc_3 = np.linspace(np.amin(data_x_3),np.amax(data_x_3),100)
y_calc_3 = np.linspace(B3,B3,100)
z_calc_3 = func_glob(x_calc_3, y_calc_3, pg_opt)
xz_calc_3 = np.column_stack((x_calc_3, z_calc_3))
np.savetxt('Data_3_OMDI_3D.fit.data',xz_calc_3,fmt='%.4e')
#get color
i = i + 1
color = (color_list[i])
# plot set 3
plt.plot(x_calc_3, z_calc_3, color)
plt.errorbar(data_x_3, data_z_3, xerr=None, yerr=data_zerr_3, fmt = color + "o")
#write Grace plot 3
c=(c+1)
d=(d+1)
draw.write("read xydy \""+str(selected_3)+"\" \n")
draw.write("s"+str(c)+" symbol "+str(d)+" \n")
draw.write("s"+str(c)+" symbol size 0.8 \n")
draw.write("s"+str(c)+" symbol color "+str(d)+" \n")
draw.write("s"+str(c)+" symbol fill color "+str(d)+" \n")
draw.write("s"+str(c)+" symbol fill pattern 1 \n")
draw.write("s"+str(c)+" errorbar color "+str(d)+" \n")
draw.write("s"+str(c)+" errorbar size 0.8 \n")
draw.write("s"+str(c)+" line type 0 \n")
c=(c+1)
e=(c-1)
fit=('Data_3_OMDI_3D.fit.data')
draw.write("read xy \""+str(fit)+"\" \n")
draw.write("s"+str(c)+" symbol 0 \n")
draw.write("s"+str(c)+" line type 1 \n")
draw.write("s"+str(c)+" line color "+str(d)+" \n")
draw.write("s"+str(c)+" layer 51 \n")
draw.write("s"+str(c)+" legend off \n")

#calculate curve 4
x_calc_4 = np.linspace(np.amin(data_x_4),np.amax(data_x_4),100)
y_calc_4 = np.linspace(B4,B4,100)
z_calc_4 = func_glob(x_calc_4, y_calc_4, pg_opt)
xz_calc_4 = np.column_stack((x_calc_4, z_calc_4))
np.savetxt('Data_4_OMDI_3D.fit.data',xz_calc_4,fmt='%.4e')
#get color
i = i + 1
color = (color_list[i])
# plot set 4
plt.plot(x_calc_4, z_calc_4, color)
plt.errorbar(data_x_4, data_z_4, xerr=None, yerr=data_zerr_4, fmt = color + "o")
#write Grace plot 4
c=(c+1)
d=(d+1)
draw.write("read xydy \""+str(selected_4)+"\" \n")
draw.write("s"+str(c)+" symbol "+str(d)+" \n")
draw.write("s"+str(c)+" symbol size 0.8 \n")
draw.write("s"+str(c)+" symbol color "+str(d)+" \n")
draw.write("s"+str(c)+" symbol fill color "+str(d)+" \n")
draw.write("s"+str(c)+" symbol fill pattern 1 \n")
draw.write("s"+str(c)+" errorbar color "+str(d)+" \n")
draw.write("s"+str(c)+" errorbar size 0.8 \n")
draw.write("s"+str(c)+" line type 0 \n")
c=(c+1)
e=(c-1)
fit=('Data_4_OMDI_3D.fit.data')
draw.write("read xy \""+str(fit)+"\" \n")
draw.write("s"+str(c)+" symbol 0 \n")
draw.write("s"+str(c)+" line type 1 \n")
draw.write("s"+str(c)+" line color "+str(d)+" \n")
draw.write("s"+str(c)+" layer 51 \n")
draw.write("s"+str(c)+" legend off \n")

#calculate curve 5
x_calc_5 = np.linspace(np.amin(data_x_5),np.amax(data_x_5),100)
y_calc_5 = np.linspace(B5,B5,100)
z_calc_5 = func_glob(x_calc_5, y_calc_5, pg_opt)
xz_calc_5 = np.column_stack((x_calc_5, z_calc_5))
np.savetxt('Data_5_OMDI_3D.fit.data',xz_calc_5,fmt='%.4e')
#get color
i = i + 1
color = (color_list[i])
# plot set 4
plt.plot(x_calc_5, z_calc_5, color)
plt.errorbar(data_x_5, data_z_5, xerr=None, yerr=data_zerr_5, fmt = color + "o")
#write Grace plot 5
c=(c+1)
d=(d+1)
draw.write("read xydy \""+str(selected_5)+"\" \n")
draw.write("s"+str(c)+" symbol "+str(d)+" \n")
draw.write("s"+str(c)+" symbol size 0.8 \n")
draw.write("s"+str(c)+" symbol color "+str(d)+" \n")
draw.write("s"+str(c)+" symbol fill color "+str(d)+" \n")
draw.write("s"+str(c)+" symbol fill pattern 1 \n")
draw.write("s"+str(c)+" errorbar color "+str(d)+" \n")
draw.write("s"+str(c)+" errorbar size 0.8 \n")
draw.write("s"+str(c)+" line type 0 \n")
c=(c+1)
e=(c-1)
fit=('Data_5_OMDI_3D.fit.data')
draw.write("read xy \""+str(fit)+"\" \n")
draw.write("s"+str(c)+" symbol 0 \n")
draw.write("s"+str(c)+" line type 1 \n")
draw.write("s"+str(c)+" line color "+str(d)+" \n")
draw.write("s"+str(c)+" layer 51 \n")
draw.write("s"+str(c)+" legend off \n")

#Plot
ax_min = np.amin(x_data) - 0.5
ax_max = np.amax(x_data) + 0.5
ay_max = np.amax(z_data) * 1.1
plt.title("OMDI")
plt.axis([ax_min,ax_max,0,ay_max])
plt.xlabel("ligand [log c]")
plt.ylabel("response")
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



log.close()

now = time.strftime("%d.%m.%Y %H:%M:%S")
res.write("\n\n"+str(now)+"\n")
res.close()
