#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:35:07 2016

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
import glob,os
import wx
import numpy as np
import matplotlib.pyplot as plt


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
y_max_max = 0

#test wheter we have files
models = len(glob.glob('*.def'))
if models == 0:
    msg = ('No model found!\n')
    err = err + msg
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    exit
if models > 1:
    msg = ('Exiting '+str(models)+'found.\n')
    err = err + msg
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    exit
count = len(glob.glob('*.dat'))
if count == 0:
    exit
else:
    for file in sorted(glob.glob('*.dat')):
        # load data
        data = np.loadtxt(file)
        x_data = data[:,0]
        y_data = data[:,1]
        x_min = np.amin(x_data)
        x_max = np.amax(x_data)
        y_min = np.amin(y_data)
        y_max = np.amax(y_data)
        if y_max > y_max_max:
            y_max_max = y_max
        if x_max > x_max_max:
            x_max_max = x_max
        if x_min < x_min_min:
            x_min_min = x_min
        #get color
        i = i + 1
        if i == 7:
            i = i - 7
        color = (color_list[i])
        # plot data
        plt.scatter(x_data, y_data, s = 16, marker = 'o', color = color)
        # find curves
        base = os.path.splitext(file)[0]
        # plot curve
        for curve in sorted(glob.glob(str(base)+'*_curve.data')):
            curve = np.loadtxt(curve)
            x_calc = curve[:,0]
            y_calc = curve[:,1]
            plt.plot(x_calc, y_calc, color)
 
#Plot atributes
for parameters in sorted(glob.glob('*.def')):
    with open(parameters) as par:
        first_line = par.readline()
        #ax_min = x_min_min - 0.5
        #ax_max = x_max_max + 0.5
        #ay_max = y_max_max * 1.1
        plt.title(str(first_line))
        #plt.axis([ax_min,ax_max,0,ay_max])
        #plt.xlabel("Allosteric modulator [log c]")
        #plt.ylabel("Tracer binding [% of control]")


#Show Plot
plt.show()
