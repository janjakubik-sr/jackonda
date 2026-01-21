#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 16:01:00 2016

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
#!/usr/bin/env python
import wx
import sys
import os.path
import preferences as pref
install_dir = (pref.install_dir)
doc_dir = (pref.doc_dir)
sys.path.append(install_dir)
sys.path.append(doc_dir)
help_file = (str(doc_dir)+'manual.txt')

class ViewerWindow(wx.Frame):
    def __init__(self, filename=''):
        super(ViewerWindow, self).__init__(None, size=(600,400))
        self.filename = filename
        self.dirname = '.'
        self.CreateInteriorWindowComponents()
        self.CreateExteriorWindowComponents()

    def CreateInteriorWindowComponents(self):
        helpfile=open(help_file, 'r')
        help=helpfile.read()
        helpfile.close()
        self.control = wx.TextCtrl(self, value=help, style=wx.TE_MULTILINE|wx.TE_READONLY)

    def CreateExteriorWindowComponents(self):
        self.CreateMenu()
#        self.CreateStatusBar()
        self.SetTitle()

    def CreateMenu(self):
        fileMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_EXIT, 'E&xit', 'Terminate the program', self.OnExit)]:
            if id == None:
                fileMenu.AppendSeparator()
            else:
                item = fileMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File') # Add the fileMenu to the MenuBar
        self.SetMenuBar(menuBar)  # Add the menuBar to the Frame

    def SetTitle(self):
        # ViewerWindow.SetTitle overrides wx.Frame.SetTitle, so we have to
        # call it using super:
        super(ViewerWindow, self).SetTitle('pyJack Documentation')


    # Event handlers:

    def OnExit(self, event):
        self.Close()  # Close the main window.


app = wx.App()
frame = ViewerWindow()
frame.Show()
app.MainLoop()
