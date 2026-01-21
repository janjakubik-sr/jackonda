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


class ViewerWindow(wx.Frame):
    def __init__(self, filename=''):
        super(ViewerWindow, self).__init__(None, size=(600,400))
        self.filename = filename
        self.dirname = '.'
        self.CreateInteriorWindowComponents()
        self.CreateExteriorWindowComponents()

    def CreateInteriorWindowComponents(self):
        self.control = wx.TextCtrl(self, value="", style=wx.TE_MULTILINE)

    def CreateExteriorWindowComponents(self):
        self.CreateMenu()
        self.CreateStatusBar()
        self.SetTitle()

    def CreateMenu(self):
        fileMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_OPEN, '&Open', 'Open a new file', self.OnOpen),
             (None, None, None, None),
             (wx.ID_EXIT, 'E&xit', 'Terminate the program', self.OnExit)]:
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
        super(ViewerWindow, self).SetTitle('Viewer %s'%self.filename)

    # Helper methods:

    def defaultFileDialogOptions(self):
        ''' Return a dictionary with file dialog options that can be
            used in both the save file dialog as well as in the open
            file dialog. '''
        return dict(message='Choose a file', defaultDir=self.dirname,
                    wildcard='*.def')

    def askUserForFilename(self, **dialogOptions):
        dialog = wx.FileDialog(self, **dialogOptions)
        if dialog.ShowModal() == wx.ID_OK:
            userProvidedFilename = True
            self.filename = dialog.GetFilename()
            self.dirname = dialog.GetDirectory()
            self.SetTitle() # Update the window title with the new filename
        else:
            userProvidedFilename = False
        dialog.Destroy()
        return userProvidedFilename
        

    # Event handlers:

    def OnExit(self, event):
        self.Close()  # Close the main window.

    def OnOpen(self, event):
        if self.askUserForFilename(style=wx.FD_OPEN,
                                   **self.defaultFileDialogOptions()):
            textfile = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(textfile.read())
            textfile.close()
        

app = wx.App()
frame = ViewerWindow()
frame.Show()
app.MainLoop()
