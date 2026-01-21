#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 13:08:33 2024

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
import os
import wx
import matplotlib.pyplot as plt
import numpy as np

#select data file
dialog = wx.FileDialog(None, "Choose input data file", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    data_file=dialog.GetPath()
dialog.Destroy()

#select x labes
dialog = wx.FileDialog(None, "Choose x labels for "+str(data_file), os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    xlabels_file=dialog.GetPath()
dialog.Destroy()

#select y labes
dialog = wx.FileDialog(None, "Choose y labels for "+str(data_file), os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    ylabels_file=dialog.GetPath()
dialog.Destroy()

# load data
data = np.loadtxt(data_file)
x = data[:,0]
y = data[:,1]
z = data[:,2]
z_min = np.amin(z)
z_max = np.amax(z)
# load labels
xlabels = np.genfromtxt(xlabels_file, dtype='str')
xN = np.size(xlabels)
xlabel_pos = np.arange(1,xN+1,1)
ylabels = np.genfromtxt(ylabels_file, dtype='str')
yN = np.size(ylabels)
ylabel_pos = np.arange(1,yN+1,1)
plt.xticks(xlabel_pos, xlabels)
plt.yticks(ylabel_pos, ylabels)
plt.scatter(x, y, s=180, c=z, cmap='RdYlBu_r', marker='s')
plt.show()

#prepare file for Grace plot
if os.path.isfile("Heat_plot.draw"):
    os.remove("Heat_plot.draw")
draw = open("Heat_plot.draw","w")

#define x step
x_step = 0.03

#define y step
y_step = 0.02

view_xmax = 0.2 + xN * x_step
view_ymin = 1.25 - yN * y_step
bar_xmin = view_xmax + 0.05
bar_xmax = view_xmax + 0.1

draw.write(" read xycsym \""+str(data_file)+"\" \n")
draw.write("    S0 type xycsym \n")
draw.write("    S0 symbol 2 \n")
draw.write("    S0 symbol size 1.00000 \n")
draw.write("    S0 symbol color 0 \n")
draw.write("    S0 symbol pattern 1 \n")
draw.write("    S0 symbol fill color 0 \n")
draw.write("    S0 symbol fill pattern 1 \n")
draw.write("    S0 symbol linestyle 0 \n")
draw.write("    S0 line type 0 \n")
draw.write("    s0 Colorbar zscale  "+str(np.floor(z_min))+" , "+str(np.ceil(z_max))+" \n")
draw.write("    s0 Colorbar nticks  6 \n")
draw.write("    s0 Colorbar     : "+str(bar_xmin)+" , 0.87 , "+str(bar_xmax)+" , 1.23 \n")
draw.write("    s0 Colorbar     linestyle 1 \n")
draw.write("    s0 Colorbar     linewidth 1.000000 \n")
draw.write("    s0 Colorbar     color 1 \n")
draw.write("    s0 Colorbar     just 1 \n")
draw.write("    s0 Colorbar     font 4 \n")
draw.write("    s0 Colorbar     char size 0.600000 \n")

draw.write("page size 595, 842 \n")
draw.write("view xmin 0.2 \n")
draw.write("view xmax "+str(view_xmax)+" \n")
draw.write("view ymin "+str(view_ymin)+" \n")
draw.write("view ymax 1.25 \n")
draw.write("world xmin 0.5 \n")
draw.write("world xmax "+str(xN+0.5)+" \n")
draw.write("world ymin 0 \n")
draw.write("world ymax "+str(yN+1)+" \n")
draw.write("  xaxis  label font \"Helvetica\" \n")
draw.write("  xaxis  label char size 0.8 \n")
draw.write("  xaxis  ticklabel font \"Helvetica\" \n")
draw.write("  xaxis  ticklabel char size 0.6 \n")
draw.write("  xaxis  ticklabel angle 0 \n")
draw.write("  yaxis  label font \"Helvetica\" \n")
draw.write("  yaxis  label char size 0.8 \n")
draw.write("  yaxis  ticklabel font \"Helvetica\" \n")
draw.write("  yaxis  ticklabel char size 0.6 \n")
draw.write("  Legend  anchor 0.22 , 0.64 \n")
draw.write("  Legend  font \"Helvetica\" \n")
draw.write("  xaxis  tick off \n")
draw.write("  xaxis  tick spec type both \n")
draw.write("  xaxis  tick spec "+str(xN)+" \n")
for i in xlabel_pos:
    draw.write("xaxis  tick major "+str(i-1)+" ,"+str(i)+" \n")
    draw.write("xaxis  ticklabel "+str(i-1)+" , \""+str(xlabels[i-1])+"\" \n")
draw.write("  yaxis  tick off \n")
draw.write("  yaxis  tick spec type both \n")
draw.write("  yaxis  tick spec "+str(yN)+" \n")
for i in ylabel_pos:
    draw.write("yaxis  tick major "+str(i-1)+" ,"+str(i)+" \n")
    draw.write("yaxis  ticklabel "+str(i-1)+" , \""+str(ylabels[i-1])+"\" \n")

draw.close()