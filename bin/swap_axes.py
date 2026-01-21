#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 12:12:20 2016

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""

import glob,os
import sys
import subprocess
import time
import wx
import numpy as np

dialog = wx.FileDialog(None, "Choose a data file to swap axes", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    data = np.loadtxt(selected)    
    columns = np.size((data)[0,:])
    rows = np.size((data)[:,0])
    if columns == 2:
        msg = ('Found 2 columns\nAssuming X Y')
        dialog = wx.MessageDialog(None, msg, 'Info', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        x_data = data[:,0]
        y_data = data[:,1]
        swapped = np.column_stack((y_data, x_data))
        np.savetxt(selected,swapped,fmt='%.4e')
    if columns == 3:
        msg = ('Found 3 columns\nAssuming X Y dY')
        dialog = wx.MessageDialog(None, msg, 'Info', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        x_data = data[:,0]
        y_data = data[:,1]
        dy_data = data[:,2]
        dx_data = [0] * rows
        swapped = np.column_stack((y_data, x_data, dy_data, dx_data))
        np.savetxt(selected,swapped,fmt='%.4e')
    if columns == 4:
        msg = ('Found 4 columns\nAssuming X Y dX dY')
        dialog = wx.MessageDialog(None, msg, 'Info', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        x_data = data[:,0]
        y_data = data[:,1]
        dx_data = data[:,2]
        dy_data = data[:,3]
        swapped = np.column_stack((y_data, x_data, dy_data, dx_data))
        np.savetxt(selected,swapped,fmt='%.4e')
    if columns not in [2., 3., 4]:
        msg = ('Wrong column count\nQuiting')
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        
log = open("temp.log","w")
log.write("... of "+str(selected))
log.close()

dialog.Destroy()
