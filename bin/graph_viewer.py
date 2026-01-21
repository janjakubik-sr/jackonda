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
count = len(glob.glob('*.dat'))
if count == 0:
    exit
else:
    for file in sorted(glob.glob('*.dat')):
        # load data
        data = np.loadtxt(file)
        x_data = data[:,0]
        y_data = data[:,1]
        y_data_err = data[:,2]
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
        plt.errorbar(x_data, y_data, xerr=None, yerr=y_data_err, fmt = color + "o")
        # find fits
        base = os.path.splitext(file)[0]
        # plot curve
        for fit in sorted(glob.glob(str(base)+'*_curve.data')):
            curve = np.loadtxt(fit)
            x_calc = curve[:,0]
            y_calc = curve[:,1]
            plt.plot(x_calc, y_calc, color)
 
#Plot atributes
j = sorted(glob.glob('*.res'))

if str(j)[2:6] == 'allo':
    ax_min = x_min_min - 0.5
    ax_max = x_max_max + 0.5
    ay_max = y_max_max * 1.1
    plt.title("Allosteric interaction")
    plt.axis([ax_min,ax_max,0,ay_max])
    plt.xlabel("Allosteric modulator [log c]")
    plt.ylabel("Tracer binding [% of control]")

if str(j)[2:7] == 'alpha':
    ax_min = x_min_min - 0.5
    ax_max = x_max_max + 0.5
    ay_max = y_max_max * 1.1
    plt.title("Meta-analysis")
    plt.axis([ax_min,ax_max,0,ay_max])
    plt.xlabel("Ligand [log c]")
    plt.ylabel("Kobs [1/min]")

if str(j)[2:7] == 'assoc':
    ax_max = x_max_max * 1.1
    ay_max = y_max_max * 1.2
    plt.title("Binding kinetics")
    plt.axis([0,ax_max,0,ay_max])
    plt.xlabel("Time [min]")
    plt.ylabel("Tracer binding [pmol / mg protein ]")

if str(j)[2:6] == 'beta':
    ax_min = x_min_min - 0.5
    ax_max = x_max_max + 0.5
    ay_max = y_max_max * 1.1
    plt.title("Interaction of 3 ligands")
    plt.axis([ax_min,ax_max,0,ay_max])
    plt.xlabel("Allosteric modulator [log c]")
    plt.ylabel("Tracer binding [% of control]")

if str(j)[2:6] == 'comp':
    ax_min = x_min_min - 0.5
    ax_max = x_max_max + 0.5
    plt.title("Competition binding")
    plt.axis([ax_min,ax_max,0,120])
    plt.xlabel("Ligand [log c]")
    plt.ylabel("Tracer binding [% of control]")

if str(j)[2:8] == 'dissoc':
    ax_max = x_max_max * 1.1
    plt.title("Binding kinetics")
    plt.axis([0,ax_max,0,120])
    plt.xlabel("Time [min]")
    plt.ylabel("Tracer binding [% of binding at time 0]")

if str(j)[2:4] == 'FR':
    ax_min = x_min_min - 0.5
    ax_max = x_max_max + 0.5
    ay_max = y_max_max * 1.1
    plt.title("Functional response")
    plt.axis([ax_min,ax_max,0,ay_max])
    plt.xlabel("Agonist [log c]")
    plt.ylabel("Response [fold over basal]")

if str(j)[2:7] == 'gamma':
    ax_min = x_min_min - 0.5
    ax_max = x_max_max + 0.5
    ay_max = y_max_max * 1.1
    plt.title("If it fits it is bitopic")
    plt.axis([ax_min,ax_max,0,ay_max])
    plt.xlabel("Allosteric modulator [log c]")
    plt.ylabel("Tracer binding [% of control]")

if str(j)[2:7] == 'satur':
    ax_max = x_max_max * 1.1
    ay_max = y_max_max * 1.2
    plt.title("Saturation binding")
    plt.axis([0,ax_max,0,ay_max])
    plt.xlabel("Free")
    plt.ylabel("Bound")

if str(j)[2:8] == 'Schild':
    ax_min = x_min_min - 0.5
    ax_max = x_max_max + 0.5
    ay_max = y_max_max + 1
    plt.title("Schild plot")
    plt.axis([ax_min,ax_max,-1,ay_max])
    plt.xlabel("Ligand [log c]")
    plt.ylabel("log (DR-1)")

#Show Plot
plt.show()
