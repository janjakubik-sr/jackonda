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

dialog = wx.FileDialog(None, "Choose a data file to sort by y values", os.getcwd(), "","*.dat", wx.FD_OPEN)
if dialog.ShowModal() == wx.ID_OK:
    selected=dialog.GetPath()
    data = np.loadtxt(selected)    
    columns = np.size((data)[0,:])
    rows = np.size((data)[:,0])
    if columns > 1:
        msg = ('Sort '+str(selected)+' by y?')
        dlg = wx.MessageDialog(None, msg, 'Sort', wx.OK|wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            x_sorted = data[np.lexsort((data[:,0], data[:,1]))]
            np.savetxt(selected,x_sorted,fmt='%.4e')
            log = open("temp.log","w")
            log.write("Data in "+str(selected)+" sorted by y values.")
            log.close()
            dlg.Destroy()
        else:
            log = open("temp.log","w")
            log.write("Sorting of "+str(selected)+" interupted.")
            log.close()        
    else:
        msg = ('Wrong column count\nQuiting')
        dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        log = open("temp.log","w")
        log.write("Error: "+str(selected)+" has wrong number of columns.")
        log.close()

dialog.Destroy()
