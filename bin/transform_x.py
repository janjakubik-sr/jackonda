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

dialog = wx.FileDialog(None, "Choose a data file to transform x values", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    data = np.loadtxt(selected)    
    columns = np.size((data)[0,:])
    rows = np.size((data)[:,0])
    if columns not in [2., 3., 4]:
        msg = ('Wrong column count\nQuiting')
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        log = open("temp.log","w")
        log.write("Error: "+str(selected)+" has wrong number of columns.")
        log.close()
    else:
        msg = ('Enter transformation formula\nfor '+str(selected)+'\n x = ')
        dlg = wx.TextEntryDialog(None, msg, defaultValue='x')
        if dlg.ShowModal() == wx.ID_OK:
            CX = dlg.GetValue()
        dlg.Destroy()
        log = open("temp.log","w")
        log.write(" of "+str(selected)+"\n by formula dy = "+str(CX))
        log.close()
        x = data[:,0]
        y = data[:,1]
        x_trans = eval(CX)
        if columns == 2:
            transformed = np.column_stack((x_trans, y))
            np.savetxt(selected,transformed,fmt='%.4e')
        if columns == 3:
            dy = data[:,2]
            transformed = np.column_stack((x_trans, y, dy))
            np.savetxt(selected,transformed,fmt='%.4e')
        if columns == 4:
            dx = data[:,2]
            dy = data[:,3]
            transformed = np.column_stack((x_trans, y, dx, dy))
            np.savetxt(selected,transformed,fmt='%.4e')

dialog.Destroy()
