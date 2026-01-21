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


dialog = wx.FileDialog(None, "Choose a data file to transform dx values", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    data = np.loadtxt(selected)    
    columns = np.size((data)[0,:])
    rows = np.size((data)[:,0])
    if columns == 4:
        msg = ('Enter transformation formula\nfor'+str(selected)+'\n dx = ')
        dlg = wx.TextEntryDialog(None, msg, defaultValue='dx')
        if dlg.ShowModal() == wx.ID_OK:
            CX = dlg.GetValue()
            dlg.Destroy()
        x = data[:,0]
        y = data[:,1]
        dx = data[:,2]
        dy = data[:,3]
        dx_trans = eval(CX)
        transformed = np.column_stack((x, y, dx_trans, dy))
        np.savetxt(selected,transformed,fmt='%.4e')
        log = open("temp.log","w")
        log.write(" of "+str(selected)+"\n by formula dx = "+str(CX))
        log.close()
    else:
        msg = ('Wrong column count\nQuiting')
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        log = open("temp.log","w")
        log.write("Error: "+str(selected)+" has wrong number of coulmns.")
        log.close()

dialog.Destroy()
