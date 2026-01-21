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
if os.path.isfile("allosteric_2_2_3D.res"):
    os.remove("allosteric_2_2_3D.res")
res = open("allosteric_2_2_3D.res","w")

#prepare file for Grace plot
if os.path.isfile("allosteric_2_2_3D.draw"):
    os.remove("allosteric_2_2_3D.draw")
draw = open("allosteric_2_2_3D.draw","w")
c=-1 #plot counter
d=0 #symbolcounter


global KA, CA, KB, KC, alpha, beta, gamma, delta, C1, C2, C3, C4

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
        label = wx.StaticText(self, -1, "3 sites: 2 allosteric ligands at 2 allosteric sites\nParameter set-up: 4 curves including control.")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer = wx.GridSizer(4, 3, 5, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Tracer KA")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.KA = wx.TextCtrl(self, -1, str(KA), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.KA, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Tracer [A]")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.CA = wx.TextCtrl(self, -1, str(CA), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.CA, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "KB")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.KB = wx.TextCtrl(self, -1, str(KB), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.KB, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "alpha")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.alpha = wx.TextCtrl(self, -1, str(alpha), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.alpha, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "KC")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.KC = wx.TextCtrl(self, -1, str(KC), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.KC, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "beta")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.beta = wx.TextCtrl(self, -1, str(beta), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.beta, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "[C]2")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.C2 = wx.TextCtrl(self, -1, str(C2), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.C2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "[C]3")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.C3 = wx.TextCtrl(self, -1, str(C3), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.C3, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        grid_sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "[C]4")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.C4 = wx.TextCtrl(self, -1, str(C4), size=(80,40), style=wx.TE_PROCESS_ENTER)
        box.Add(self.C4, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
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
CA = 100e-12
KA = 250e-12
KB = 1e-8
KC = 1e-6
alpha = 0.2
beta = 10

#define four concetrations of B, C1 should be zero
C1 = 0.000
C2 = 3e-7
C3 = 1e-6
C4 = 3e-6

#set estimates and bounds
gamma_ini = 1
gamma_min = 0.01
gamma_max = 100
delta_ini = 1
delta_min =0.01
delta_max = 100

dlg = Estimates(None, -1, "Enter system parameters for 4 curves including control.", size=(350, 300),
               #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
               style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
               )
dlg.CenterOnScreen()
val = dlg.ShowModal()
if val == wx.ID_OK:
    KA = float(dlg.KA.GetValue())
    KB = float(dlg.KB.GetValue())
    KC = float(dlg.KC.GetValue())
    alpha = float(dlg.alpha.GetValue())
    beta = float(dlg.beta.GetValue())
    CA = float(dlg.CA.GetValue())
    C2 = float(dlg.C2.GetValue())
    C3 = float(dlg.C3.GetValue())
    C4 = float(dlg.C4.GetValue())
else:
    msg = ("Fitting was canceled.")
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    log.write("Error: Fitting was canceled")
    tolog = log.read()
    None.__log(tolog)

#select files
dialog = wx.FileDialog(None, "Choose a control curve, [C] = "+str(C1)+"\n", os.getcwd(), "","*.dat", wx.FD_OPEN)
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

dialog = wx.FileDialog(None, "Choose a curve with the lowest concentration, [C] = "+str(C2)+"\n", os.getcwd(), "","*.dat", wx.FD_OPEN)
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

dialog = wx.FileDialog(None, "Choose a curve with the intermediate concentration, [C] = "+str(C3)+"\n", os.getcwd(), "","*.dat", wx.FD_OPEN)
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

dialog = wx.FileDialog(None, "Choose a control the highest concentration, [C] = "+str(C4)+"\n", os.getcwd(), "","*.dat", wx.FD_OPEN)
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

#load data
data_1 = np.loadtxt(selected_1)
data_2 = np.loadtxt(selected_2)
data_3 = np.loadtxt(selected_3)
data_4 = np.loadtxt(selected_4)

#create 3D data set
data_x_1 = data_1[:,0]
data_y_1 = np.linspace(C1,C1,len(data_1))
data_z_1 = data_1[:,1]
data_zerr_1 = data_1[:,2]
data_x_2 = data_2[:,0]
data_y_2 = np.linspace(C2,C2,len(data_2))
data_z_2 = data_2[:,1]
data_zerr_2 = data_2[:,2]
data_x_3 = data_3[:,0]
data_y_3 = np.linspace(C3,C3,len(data_3))
data_z_3 = data_3[:,1]
data_zerr_3 = data_3[:,2]
data_x_4 = data_4[:,0]
data_y_4 = np.linspace(C4,C4,len(data_4))
data_z_4 = data_4[:,1]
data_zerr_4 = data_4[:,2]
x_data = np.concatenate((data_x_1,data_x_2,data_x_3,data_x_4),axis=None)
y_data = np.concatenate((data_y_1,data_y_2,data_y_3,data_y_4),axis=None)
z_data = np.concatenate((data_z_1,data_z_2,data_z_3,data_z_4),axis=None)
z_data_err = np.concatenate((data_zerr_1,data_zerr_2,data_zerr_3,data_zerr_4),axis=None)

#fit data
p1 = [gamma_ini, delta_ini]
#Define global fit function
def func_glob(x, y, p):
    gamma, delta = p
    return 100 * (CA + KA) / (CA + KA * (1 + (10**x) / KB + y / KC * (1 + (10**x) / gamma / KB) ) / (1 + (10**x) / alpha / KB + y / beta / KC * (1 + (10**x) / alpha / gamma / delta / KB ) ) )
def err(p, x, y, z):
    return func_glob(x, y, p) - z

pg_estim = p1
pg_opt, cov_x, infodict, errmsg, success = opt.leastsq(err, pg_estim, args=(x_data, y_data, z_data), full_output=1, epsfcn=0.0001)
residuals = err(pg_opt, x_data, y_data, z_data)
reduced_chi_square = np.sum(residuals**2)/(len(x_data)-3)
pg_cov = cov_x * reduced_chi_square
pg_err = np.sqrt(np.diag(pg_cov))
gamma_calc = (pg_opt[0])
gamma_err = (pg_err[0])
delta_calc = (pg_opt[1])
delta_err = (pg_err[1])
gamma_res = (str("{0:.4f}".format(gamma_calc))+" ± "+str("{0:.4f}".format(gamma_err)))
delta_res = (str("{0:.4f}".format(delta_calc))+" ± "+str("{0:.4f}".format(delta_err)))

#prepare file for writing results
res.write("3 sites: 2 allosteric ligands at 2 allosteric sites\n\n")
res.write("KB = "+str(KB)+"\nalpha = "+str(alpha)+"\nKC = "+str(KC)+"\nbeta = "+str(beta)+"\nKA = "+str(KA)+"\n[A]"+str(CA)+"\n\n")
res.write("3D fit\n")
res.write("gamma = "+str(gamma_res)+"\ndelta = "+str(delta_res)+"\n")

#calculate curve 1
x_calc_1 = np.linspace(np.amin(data_x_1),np.amax(data_x_1),100)
y_calc_1 = np.linspace(C1,C1,100)
z_calc_1 = func_glob(x_calc_1, y_calc_1, pg_opt)
xz_calc_1 = np.column_stack((x_calc_1, z_calc_1))
np.savetxt('Data_A_allosteric_2_2_3D.fit.data',xz_calc_1,fmt='%.4e')
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
draw.write("s"+str(c)+" legend \" \\f{Symbol}g\\f{}="+str("{0:.2f}".format(gamma_calc))+' \\#{B1} '+str("{0:.2f}".format(gamma_err))+" \\f{Symbol}d\\f{}="+str("{0:.2f}".format(delta_calc))+' \\#{B1} '+str("{0:.2f}".format(delta_err))+"\" \n")
c=(c+1)
e=(c-1)
fit=('Data_A_allosteric_2_2_3D.fit.data')
draw.write("read xy \""+str(fit)+"\" \n")
draw.write("s"+str(c)+" symbol 0 \n")
draw.write("s"+str(c)+" line type 1 \n")
draw.write("s"+str(c)+" line color "+str(d)+" \n")
draw.write("s"+str(c)+" layer 51 \n")
draw.write("s"+str(c)+" legend off \n")

#calculate curve 2
x_calc_2 = np.linspace(np.amin(data_x_2),np.amax(data_x_2),100)
y_calc_2 = np.linspace(C2,C2,100)
z_calc_2 = func_glob(x_calc_2, y_calc_2, pg_opt)
xz_calc_2 = np.column_stack((x_calc_2, z_calc_2))
np.savetxt('Data_B_allosteric_2_2_3D.fit.data',xz_calc_2,fmt='%.4e')
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
fit=('Data_B_allosteric_2_2_3D.fit.data')
draw.write("read xy \""+str(fit)+"\" \n")
draw.write("s"+str(c)+" symbol 0 \n")
draw.write("s"+str(c)+" line type 1 \n")
draw.write("s"+str(c)+" line color "+str(d)+" \n")
draw.write("s"+str(c)+" layer 51 \n")
draw.write("s"+str(c)+" legend off \n")

#calculate curve 3
x_calc_3 = np.linspace(np.amin(data_x_3),np.amax(data_x_3),100)
y_calc_3 = np.linspace(C3,C3,100)
z_calc_3 = func_glob(x_calc_3, y_calc_3, pg_opt)
xz_calc_3 = np.column_stack((x_calc_3, z_calc_3))
np.savetxt('Data_C_allosteric_2_2_3D.fit.data',xz_calc_3,fmt='%.4e')
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
fit=('Data_C_allosteric_2_2_3D.fit.data')
draw.write("read xy \""+str(fit)+"\" \n")
draw.write("s"+str(c)+" symbol 0 \n")
draw.write("s"+str(c)+" line type 1 \n")
draw.write("s"+str(c)+" line color "+str(d)+" \n")
draw.write("s"+str(c)+" layer 51 \n")
draw.write("s"+str(c)+" legend off \n")

#calculate curve 4
x_calc_4 = np.linspace(np.amin(data_x_4),np.amax(data_x_4),100)
y_calc_4 = np.linspace(C4,C4,100)
z_calc_4 = func_glob(x_calc_4, y_calc_4, pg_opt)
xz_calc_4 = np.column_stack((x_calc_4, z_calc_4))
np.savetxt('Data_D_allosteric_2_2_3D.fit.data',xz_calc_4,fmt='%.4e')
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
fit=('Data_D_allosteric_2_2_3D.fit.data')
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
plt.title("Allosteric interaction 3D-fit")
plt.axis([ax_min,ax_max,0,ay_max])
plt.xlabel("ligand [log c]")
plt.ylabel("tracer binding")
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
draw.write("xaxis label \"log[B]\"  \n")
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

log.close()

now = time.strftime("%d.%m.%Y %H:%M:%S")
res.write("\n\n"+str(now)+"\n")
res.close()
