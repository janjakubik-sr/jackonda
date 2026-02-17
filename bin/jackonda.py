#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 16:01:00 2016

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
#!/usrenv python
import wx
import os
import sys
import subprocess
import time
import numpy as np

import preferences as pref
install_dir = (pref.install_dir)
sys.path.append(install_dir)
doc_dir = (pref.doc_dir)
sys.path.append(doc_dir)
example_dir = (pref.example_dir)
sys.path.append(example_dir)
width = (pref.width)
height = (pref.height)

#temp file
if os.path.isfile("nc.tmp"):
    os.remove("nc.tmp")

def exec_full(filepath):
    global_namespace = {
        "__file__": filepath,
        "__name__": "__main__",
    }
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), global_namespace)


welcome = "\n******************************************\nHello, welcome to Jackonda\nAll-in-One jack for molecular pharmacology written in Python\nby Jan Jakubik jan.jakubik@fgu.cas.cz\nCreative Commons Licence BY-NC\n*****************************************\n"

stamp = time.strftime("%Y%m%d%H%M%S")
class MainWindow(wx.Frame):
    def __init__(self, filename=(stamp+'.log')):
        super(MainWindow, self).__init__(None, size=(width,height))
        self.filename = filename
        self.dirname = '.'
        self.CreateInteriorWindowComponents()
        self.CreateExteriorWindowComponents()

    def CreateInteriorWindowComponents(self):
        self.logger = wx.TextCtrl(self, value=welcome, style=wx.TE_MULTILINE|wx.TE_READONLY)
        
    def CreateExteriorWindowComponents(self):
        self.CreateMenu()
        self.CreateStatusBar()
        self.SetTitle()

    def CreateMenu(self):
        fileMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_SAVE, '&Save log', 'Save the current log file', self.OnSave),
             (wx.ID_OPEN, '&Working Directory', 'Change working directory', self.OnCWD),
             (wx.ID_PREFERENCES, 'Preferences', 'Define default aplications, etc.', self.OnPrefs),
             (wx.ID_EXIT, 'E&xit', 'Terminate the program', self.OnExit)
            ]:
            if id == None:
                fileMenu.AppendSeparator()
            else:
                item = fileMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)

        dataMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'Edit in text editor', 'Edit data', self.OnEdit),
            (wx.ID_ANY, 'Sort data by X', 'Sort data by value of x', self.OnSortX),
            (wx.ID_ANY, 'Sort data by Y', 'Sort data by value of y', self.OnSortY),
            (wx.ID_ANY, 'Swap X and Y', 'Swap axes', self.OnTransformSwap),
            (wx.ID_ANY, 'Transform X', 'Transform X', self.OnTransformX),
            (wx.ID_ANY, 'Transform Y', 'Transform Y', self.OnTransformY),
            (wx.ID_ANY, 'Transform dX', 'Transform dX', self.OnTransformDX),
            (wx.ID_ANY, 'Transform dY', 'Transform dY', self.OnTransformDY)
	       ]:
            if id == None:
                dataMenu.AppendSeparator()
            else:
                item = dataMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)

        batchMenu = wx.Menu()
        subMenu1 = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'Saturation of a single site', 'Analyze data', self.OnTask10),
	        (wx.ID_ANY, 'Saturation of two sites', 'Analyze data', self.OnTask11),
	        (wx.ID_ANY, 'Competition for a single site', 'Analyze data', self.OnTask12),
            (wx.ID_ANY, 'Competition for a single site, Beq', 'Analyze data', self.OnTask12b),
	        (wx.ID_ANY, 'Competition for two sites', 'Analyze data', self.OnTask13),
	        (wx.ID_ANY, 'Competition with low-affinity ligand', 'Analyze data', self.OnTask14),
            (wx.ID_ANY, 'Competition screenig', 'Analyze data', self.OnTask14b),
	        (wx.ID_ANY, 'Allosteric interaction', 'Analyze data', self.OnTask15),
            (wx.ID_ANY, 'Dualsteric interaction', 'Analyze data', self.OnTask15b),
	        (wx.ID_ANY, '3-ligands: tracer, competitive and allosteric', 'Analyze data', self.OnTask16),
	        (wx.ID_ANY, '3-ligands: tracer, bitopic and allosteric', 'Analyze data', self.OnTask17),
            (wx.ID_ANY, '3-ligands: tracer, 2 allosteric at 1 site', 'Analyze data', self.OnTask18a),
            (wx.ID_ANY, '3-ligands: tracer, 2 allosteric at 2 sites', 'Analyze data', self.OnTask18b),
            (wx.ID_ANY, '3-ligands: tracer, 2 allosteric at 2 sites - gamma, delta 3D-fit', 'Analyze data', self.OnTask18c),
            (wx.ID_ANY, '3-ligands: tracer and 1 allosteric at 2 sites - full', 'Analyze data', self.OnTask19a),
            (wx.ID_ANY, '3-ligands: tracer and 1 allosteric at 2 sites - simplified delta=1', 'Analyze data', self.OnTask19b),
            (wx.ID_ANY, '3-ligands: tracer and 1 allosteric at 2 sites - simplified gamma.delta=1', 'Analyze data', self.OnTask19c),
            ]:
            if id == None:
                subMenu1.AppendSeparator()
            else:
                item = subMenu1.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        batchMenu.AppendSubMenu(subMenu1,"Equilibrium binding")

        subMenu2 = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'Association with one site', 'Analyze data', self.OnTask20),
             (wx.ID_ANY, 'Association with two sites', 'Analyze data', self.OnTask21),
             (wx.ID_ANY, 'Dissociation from one site - normalized', 'Analyze data', self.OnTask22),
             (wx.ID_ANY, 'Dissociation from one site - Koff, Beq', 'Analyze data', self.OnTask22b),
             (wx.ID_ANY, 'Dissociation from two sites', 'Analyze data', self.OnTask23),
             (wx.ID_ANY, 'Dissociation from sites, one rate fixed', 'Analyze data', self.OnTask24),
             ]:
            if id == None:
                subMenu2.AppendSeparator()
            else:
                item = subMenu2.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        batchMenu.AppendSubMenu(subMenu2,"Kinetics")

        subMenu3 = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'FR - single effector - fold over basal', 'Analyze data', self.OnTask30),
             (wx.ID_ANY, 'FR - single effector - FOB screen', 'Analyze data', self.OnTask30s),
             (wx.ID_ANY, 'FR - single effector - absolute increase', 'Analyze data', self.OnTask30a),
             (wx.ID_ANY, 'FR - single effector - abs. increase screen', 'Analyze data', self.OnTask30as),
             (wx.ID_ANY, 'FR - single effector - %MPE', 'Analyze data', self.OnTask30b),
             (wx.ID_ANY, 'FR - single effector - variable basal', 'Analyze data', self.OnTask31),
             (wx.ID_ANY, 'FR - single effector - variable basal + fixed Emax', 'Analyze data', self.OnTask31a),
             (wx.ID_ANY, 'FR - two effectors - double S-shape', 'Analyze data', self.OnTask32),
             (wx.ID_ANY, 'FR- two effectors - U-shape', 'Analyze data', self.OnTask33),
             (wx.ID_ANY, 'FR - two effectors - bell-shape', 'Analyze data', self.OnTask34),
             (wx.ID_ANY, 'OMA - tau, Emax ', 'Analyze data', self.OnTask35),
             (wx.ID_ANY, 'OMA - tau, Ka ', 'Analyze data', self.OnTask36),
             (wx.ID_ANY, 'OMA - tau only ', 'Analyze data', self.OnTask37),
             (wx.ID_ANY, 'OMAMA - alpha, beta 3D-fit', 'Oparational Model of Allosterically Modulated Agonism', self.OnTask38),
             (wx.ID_ANY, 'OMDI - KB, KC, alpha, beta, gamma 3D-fit', 'Operational model of Dualsteric Inhibition', self.OnTask38a),
             (wx.ID_ANY, 'OMARD - alpha, beta, gamma', 'Operational model of Receptor Dimers', self.OnTask39),
             (wx.ID_ANY, 'OMARD - receptor depletion', 'Operational Model of Receptor Dimers', self.OnTask39a),
             ]:
            if id == None:
                subMenu3.AppendSeparator()
            else:
                item = subMenu3.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        batchMenu.AppendSubMenu(subMenu3,"Functional response")

        subMenu4 = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'alphaKD from Koffs', 'Analyze data', self.OnTask40),
            (wx.ID_ANY, 'Schild analysis - allosteric antagonism', 'Analyze data', self.OnTask41),
            (wx.ID_ANY, 'Schild analysis - competitive antagonism', 'Analyze data', self.OnTask42),
            (wx.ID_ANY, "tau, Emax and pKa from EC50 and E\'max - Operational model", 'Analyze data', self.OnTask43),
            ]:
            if id == None:
                subMenu4.AppendSeparator()
            else:
                item = subMenu4.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        batchMenu.AppendSubMenu(subMenu4,"Meta-analysis")

        interMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'Allosteric interaction', 'Analyze data from competition-like experiment', self.OnTask50),
             (wx.ID_ANY, 'Association', 'Analyze data from saturation experiment', self.OnTask51),
             (wx.ID_ANY, 'Competitive interaction', 'Analyze data from competition experiment', self.OnTask52),
             (wx.ID_ANY, 'Dissociation', 'Analyze data from dissociation experiment', self.OnTask53),
             (wx.ID_ANY, 'Functional response - monophasic', 'Analyze data of functional response to agonist', self.OnTask54a),
             (wx.ID_ANY, 'Functional response - biphasic', 'Analyze data of functional response to agonist', self.OnTask54),
             (wx.ID_ANY, 'OMA - Partial agonist - tau, Emax', 'Analyze data', self.OnTask55),
             (wx.ID_ANY, 'OMA - Partial agonist - tau, Emax, pKa', 'Analyze data', self.OnTask56),
             (wx.ID_ANY, 'OMA - Receptor depletion - tau, Emax', 'Analyze data', self.OnTask57),
             (wx.ID_ANY, 'OMA - Receptor depletion - tau, Emax, pKa', 'Analyze data', self.OnTask58),
             (wx.ID_ANY, 'OMARD - Receptor depletion - tau, Emax, pKa', 'Analyze data', self.OnTask58aa),
             (wx.ID_ANY, 'Saturation - one site', 'Analyze data from saturation experiment', self.OnTask59a),
             (wx.ID_ANY, 'Saturation - two sites', 'Analyze data from saturation experiment', self.OnTask59),
	      ]:
            if id == None:
                interMenu.AppendSeparator()
            else:
                item = interMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)

        modelMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'Allosteric interaction of 3 ligands', 'Model interaction of 3 ligands', self.OnModel3L),
             (wx.ID_ANY, 'OMA - Operational Model of Agonism', 'Model functional response', self.OnModelOMA),
             (wx.ID_ANY, 'OMAMA - Operational Model of Allosterically Modulated Agonism', 'Model allosterically modulated agonism', self.OnModelOMAMA),
             (wx.ID_ANY, 'OMAFB - Operational Model with Signal Feedback - delta', 'Model functional response', self.OnModelOMAFBdelta),
             (wx.ID_ANY, 'OMAFB - Operational Model with Signal Feedback - tau', 'Model functional response', self.OnModelOMAFBtau),
             (wx.ID_ANY, 'OMANCI - Operational Model Non-competitive Auto-inhibition - Ke', 'Model functional response', self.OnModelOMANCIKe),
             (wx.ID_ANY, 'OMANCI - Operational Model Non-competitive Auto-inhibition - Ki', 'Model functional response', self.OnModelOMANCIKi),
             (wx.ID_ANY, 'OMANCI - Operational Model Non-competitive Auto-inhibition - Rtot', 'Model functional response', self.OnModelOMANCIRtot),
             (wx.ID_ANY, 'OMALE - Operational Model of Low Expression - Ke', 'Model functional response', self.OnModelOMALEK),
             (wx.ID_ANY, 'OMALE - Operational Model of Low Expression - Rtot', 'Model functional response', self.OnModelOMALER),
             (wx.ID_ANY, 'OMARD - OMA at Receptor Dimers - alpha', 'Model functional response', self.OnModelOMARDa),
             (wx.ID_ANY, 'OMARD - OMA at Receptor Dimers - beta', 'Model functional response', self.OnModelOMARDb),
             (wx.ID_ANY, 'OMARD - OMA at Receptor Dimers - Rtot', 'Model functional response', self.OnModelOMARDr),
             (wx.ID_ANY, 'OMASI - Operational Model Substrate Inhibition - Ke', 'Model functional response', self.OnModelOMASIKe),
             (wx.ID_ANY, 'OMASI - Operational Model Substrate Inhibition - Ki', 'Model functional response', self.OnModelOMASIKi),
             (wx.ID_ANY, 'OMASI - Operational Model Substrate Inhibition - Rtot', 'Model functional response', self.OnModelOMASIRtot),
             (wx.ID_ANY, 'View Model Graph', 'View Model Graph', self.OnModelView),
             (wx.ID_ANY, 'View Model Parameters', 'View Model Paramaters', self.OnModelPar),
	      ]:
            if id == None:
                modelMenu.AppendSeparator()
            else:
                item = modelMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        

        resMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'Plot results with Grace', 'Plot results with grace', self.OnTaskPlot),
             (wx.ID_ANY, 'View Grace graph', 'Open graph in grace', self.OnShowGraph),
             (wx.ID_ANY, 'View results plot', 'View results file in viewer', self.OnShowPlot),
             (wx.ID_ANY, 'View results table', 'View results file in viewer', self.OnShowRes),
             (wx.ID_ANY, 'XYCSym', 'Heat plot as XYCSym', self.OnTaskColorbat),
	      ]:
            if id == None:
                resMenu.AppendSeparator()
            else:
                item = resMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)

                
        appMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ANY, 'IPython', 'Open IPython console', self.OnTaskIP),
            (wx.ID_ANY, 'Plotting (Grace)', 'Open Grace', self.OnTaskGG),
            (wx.ID_ANY, 'Statistics (R)', 'Open R console', self.OnTaskR),
            (wx.ID_ANY, 'Spreadsheet (pyspread)', 'Open shell console', self.OnTaskSpread),
            (wx.ID_ANY, 'Terminal (Shell)', 'Open shell console', self.OnTaskSh),
	      ]:
            if id == None:
                appMenu.AppendSeparator()
            else:
                item = appMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)

        helpMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_HELP, '&Help', 'Help', self.OnHelp),
             (wx.ID_HELP_INDEX, 'Examples', 'Examples', self.OnExample),
             (wx.ID_ABOUT, '&About', 'Information about this program', self.OnAbout),]:
            if id == None:
                helpMenu.AppendSeparator()
            else:
                item = helpMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
                
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, 'File')
        menuBar.Append(dataMenu, 'Data Transformation')
        menuBar.Append(batchMenu, 'Batch Analysis')
        menuBar.Append(interMenu, 'Interactive Analysis')
        menuBar.Append(modelMenu, 'Models')
        menuBar.Append(resMenu, 'Results')
        menuBar.Append(appMenu, 'Auxilary Apps')
        menuBar.Append(helpMenu, 'Help')
        self.SetMenuBar(menuBar)

    def SetTitle(self):
        # MainWindow.SetTitle overrides wx.Frame.SetTitle, so we have to
        # call it using super:
        super(MainWindow, self).SetTitle('Jackonda')

    # Helper method(s):

    def __log(self, message):
        ''' Private method to append a string to the logger text
            control. '''
        self.logger.AppendText('%s\n'%message)

    # Event handlers:
    def OnAbout(self, event):
        dialog = wx.MessageDialog(self, 'Little pharmacological data analysis app written in python by Jan Jakubik. Non-commercial use allowed under Creative commons licence (BY-NC).', 'About This App', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def OnCWD(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           | wx.DD_DIR_MUST_EXIST
                           | wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            new_dir = dlg.GetPath()
            self.__log('Current dir is '+str(new_dir))
            os.chdir(new_dir)
            if os.path.isfile("nc.tmp"):
                os.remove("nc.tmp")
            dlg.Destroy()

    def OnPrefs(self, event):
        cmd = ('python '+str(install_dir)+'prefs.py')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        
    def OnHelp(self, event):
        cmd = ('python '+str(install_dir)+'help.py')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnExample(self, event):
        dlg = wx.DirDialog(self, "Choose a directory with examples:",
                           defaultPath=example_dir,
                           style=wx.DD_DEFAULT_STYLE
                           | wx.DD_DIR_MUST_EXIST
                           | wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            new_dir = dlg.GetPath()
            self.__log('Current dir is '+str(new_dir))
            os.chdir(new_dir)
            dlg.Destroy()

    def OnExit(self, event):
        self.Close()  # Close the main window.

    def OnSave(self, event):
        textfile = open(os.path.join(self.dirname, self.filename), 'w')
        textfile.write(self.logger.GetValue())
        textfile.close()

    def OnEdit(self, event):
        cmd = ('python '+str(install_dir)+'editor.py')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnSortX(self, event):
        self.__log('Sorting by X values')
        exec_full(str(install_dir)+'sort_by_x.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnSortY(self, event):
        self.__log('Sorting by Y values')
        exec_full(str(install_dir)+'sort_by_y.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTransformSwap(self, event):
        self.__log('Swapping X and Y axes ...')
        exec_full(str(install_dir)+'swap_axes.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTransformX(self, event):
        self.__log('Transforming X values')
        exec_full(str(install_dir)+'transform_x.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTransformY(self, event):
        self.__log('Transforming Y values')
        exec_full(str(install_dir)+'transform_y.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTransformDY(self, event):
        self.__log('Transforming dY values')
        exec_full(str(install_dir)+'transform_dy.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTransformDX(self, event):
        self.__log('Transforming dX values')
        exec_full(str(install_dir)+'transform_dx.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTransform(self, event):
        cmd = ('glue')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        
    def OnShowRes(self, event):
        cmd = ('python '+str(install_dir)+'viewer.py')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnShowPlot(self, event):
        cmd = ('python '+str(install_dir)+'graph_viewer.py')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnShowGraph(self, event):
        dialog = wx.FileDialog(self, "Choose Grace file to open", os.getcwd(), "","*.agr", wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            selected=dialog.GetPath()
            cmd = (str(pref.cmdGG)+" "+str(selected))
            subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        dialog.Destroy()
        
    def OnTaskPlot(self, event):
        dialog = wx.FileDialog(self, "Choose a draw file to plot with Grace", os.getcwd(), "","*.draw", wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            selected=dialog.GetPath()
            cmd = (str(pref.cmdGB)+" "+str(selected))
            subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        dialog.Destroy()

    def OnTaskColorbat(self, event):
        self.__log('Heat plot view ...')
        exec_full(str(install_dir)+'colorbat.py')

    def OnTaskIP(self, event):
        subprocess.Popen(pref.cmdIP, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnTaskGG(self, event):
        subprocess.Popen(pref.cmdGG, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnTaskR(self, event):
        subprocess.Popen(pref.cmdR, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnTaskSh(self, event):
        subprocess.Popen(pref.cmdSh, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnTaskSpread(self, event):
        subprocess.Popen(pref.cmdspread, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnTask(self, event):
        dialog = wx.MessageDialog(self, 'Not implemented yet.', 'Ehm', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    
    def OnTask10(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'saturation_1.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('saturation_1.res','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnTask11(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'saturation_2.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('saturation_2.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask12(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'competition_1.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('competition_1.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask12b(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'competition_1b.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('competition_1b.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask13(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'competition_2.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('competition_2.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask14(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'competition_0.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('competition_0.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask14b(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'competition_s.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('competition_s.res','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnTask15(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'allosteric.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('allosteric.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask15b(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'dualsteric.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('dualsteric.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask16(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'beta.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('beta.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask17(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'gamma.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('gamma.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask18a(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'allosteric_2_1.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('allosteric_2_1.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask18b(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'allosteric_2_2.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('allosteric_2_2.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask18c(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'allosteric_2_2_3D.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('allosteric_2_2_3D.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask19a(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'allosteric_1_2.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('allosteric_1_2.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask19b(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'allosteric_1_2d.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('allosteric_1_2d.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask19c(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'allosteric_1_2s.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('allosteric_1_2s.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask19d(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'allosteric_1_2_3D.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('allosteric_1_2_3D.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask20(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'association_1.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('association_1.res','r')
        tolog = log.read()
        self.__log(tolog)
    
    def OnTask21(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'association_2.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('association_2.res','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnTask22(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'dissociation_1.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('dissociation_1.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask22b(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'dissociation_1b.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('dissociation_1b.res','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnTask23(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'dissociation_2.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('dissociation_2.res','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnTask24(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'dissociation_2f.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('dissociation_2f.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask30(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'FR.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask30s(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'FR_s.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_s.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask30a(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'FR_0.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_0.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask30as(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'FR_0s.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_0s.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask30b(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'FR_MPE.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_MPE.res','r')
        tolog = log.read()
        self.__log(tolog)
    
    def OnTask31(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'FR_X.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_X.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask31a(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'FR_XE.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_XE.res','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnTask32(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'FR_S.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_S.res','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnTask33(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'FR_U.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_U.res','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnTask34(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'FR_B.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_B.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask35(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'FR_OM_1.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_OM_1.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask36(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'FR_OM_2.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_OM_2.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask37(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'FR_OM_3.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_OM_3.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask38(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'FR_OMAMA.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_OMAMA_3D.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask38a(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'FR_OMDI.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_OMDI_3D.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask39(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'FR_OMARD.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_OMARD.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask39a(self, event):
        self.__log('Batch processing ...')
        dlg = DataSets(self, -1, "OMARD - Receptor depletion", size=(350, 200),
                       #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                       style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
                       )
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            curves = np.loadtxt('nc.tmp')
            os.remove('nc.tmp')
            if curves == 2:
                exec_full(str(install_dir)+'FR_OMARD_RD_2.py')
            else:
                if curves == 3:
                    exec_full(str(install_dir)+'FR_OMARD_RD_3.py')
                else:
                    if curves == 4:
                        exec_full(str(install_dir)+'FR_OMARD_RD_4.py')
                    else:
                        if curves == 5:
                            exec_full(str(install_dir)+'FR_OMARD_RD_5.py')
                        else:
                            msg = ('Wrong number of curves\n')
                            dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
                            dialog.ShowModal()
                            dialog.Destroy()
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_OMARD_RD.res','r')
        tolog = log.read()
        self.__log(tolog)


    def OnTask40(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'alpha_KD.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('alpha_KD.res','r')
        tolog = log.read()
        self.__log(tolog)
    
    def OnTask41(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'Schild_alloster.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('Schild_alloster.res','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnTask42(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'Schild_compet.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('Schild_compet.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask43(self, event):
        self.__log('Batch processing ...')
        dlg = DataSets(self, -1, "Emax, tau and Ka from logEC50 and E'max", size=(350, 200),
                       #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                       style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
                       )
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            curves = np.loadtxt('nc.tmp')
            os.remove('nc.tmp')
            if curves == 1:
                exec_full(str(install_dir)+'FR_to_OM_1.py')
            else:
                if curves == 2:
                    exec_full(str(install_dir)+'FR_to_OM_2.py')
                else:
                    if curves == 3:
                        exec_full(str(install_dir)+'FR_to_OM_3.py')
                    else:
                        if curves == 4:
                            exec_full(str(install_dir)+'FR_to_OM_4.py')
                        else:
                            if curves == 5:
                                exec_full(str(install_dir)+'FR_to_OM_5.py')
                            else:
                                msg = ('Wrong number of curves\n')
                                dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
                                dialog.ShowModal()
                                dialog.Destroy()
        else:
            msg = ('Test was canceled.')
            dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
            log = open("temp.log","w")
            log.write("Error: Test was canceled")
            log.close()
            tolog = log.read()
            self.__log(tolog)
        dlg.Destroy()
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_to_OM.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask50(self, event):
        self.__log('Interactive analysis ...')
        exec_full(str(install_dir)+'allosteric_i.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnTask51(self, event):
        self.__log('Interactive analysis ...')
        exec_full(str(install_dir)+'association_i.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnTask52(self, event):
        self.__log('Interactive analysis ...')
        exec_full(str(install_dir)+'competition_i.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnTask53(self, event):
        self.__log('Interactive analysis ...')
        exec_full(str(install_dir)+'dissociation_i.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask54a(self, event):
        self.__log('Interactive analysis ...')
        exec_full(str(install_dir)+'FR_i_s.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask54(self, event):
        self.__log('Interactive analysis ...')
        exec_full(str(install_dir)+'FR_i.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask55(self, event):
        self.__log('Batch processing ...')
        dlg = DataSets(self, -1, "Operational Model - Partial agonist", size=(350, 200),
                       #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                       style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
                       )
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            curves = np.loadtxt('nc.tmp')
            os.remove('nc.tmp')
            if curves == 2:
                exec_full(str(install_dir)+'FR_OM_PA_2.py')
            else:
                if curves == 3:
                    exec_full(str(install_dir)+'FR_OM_PA_3.py')
                else:
                    if curves == 4:
                        exec_full(str(install_dir)+'FR_OM_PA_4.py')
                    else:
                        if curves == 5:
                            exec_full(str(install_dir)+'FR_OM_PA_5.py')
                        else:
                            msg = ('Wrong number of curves\n')
                            dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
                            dialog.ShowModal()
                            dialog.Destroy()
        else:
            msg = ('Analysis was canceled.')
            dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
            log = open("temp.log","w")
            log.write("Error: Test was canceled")
            log.close()
            tolog = log.read()
            self.__log(tolog)
        dlg.Destroy()
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_OM_PA.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask56(self, event):
        self.__log('Batch processing ...')
        dlg = DataSets(self, -1, "Operational Model - Partial agonist", size=(350, 200),
                       #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                       style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
                       )
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            curves = np.loadtxt('nc.tmp')
            os.remove('nc.tmp')
            if curves == 2:
                exec_full(str(install_dir)+'FR_OM_PA_a_2.py')
            else:
                if curves == 3:
                    exec_full(str(install_dir)+'FR_OM_PA_a_3.py')
                else:
                    if curves == 4:
                        exec_full(str(install_dir)+'FR_OM_PA_a_4.py')
                    else:
                        if curves == 5:
                            exec_full(str(install_dir)+'FR_OM_PA_a_5.py')
                        else:
                            msg = ('Wrong number of curves\n')
                            dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
                            dialog.ShowModal()
                            dialog.Destroy()
        else:
            msg = ('Analysis was canceled.')
            dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
            log = open("temp.log","w")
            log.write("Error: Test was canceled")
            log.close()
            tolog = log.read()
            self.__log(tolog)
        dlg.Destroy()
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_OM_PA.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask57(self, event):
        self.__log('Batch processing ...')
        dlg = DataSets(self, -1, "Operational Model - Receptor depletion", size=(350, 200),
                       #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                       style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
                       )
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            curves = np.loadtxt('nc.tmp')
            os.remove('nc.tmp')
            if curves == 2:
                exec_full(str(install_dir)+'FR_OM_RD_2.py')
            else:
                if curves == 3:
                    exec_full(str(install_dir)+'FR_OM_RD_3.py')
                else:
                    if curves == 4:
                        exec_full(str(install_dir)+'FR_OM_RD_4.py')
                    else:
                        if curves == 5:
                            exec_full(str(install_dir)+'FR_OM_RD_5.py')
                        else:
                            msg = ('Wrong number of curves\n')
                            dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
                            dialog.ShowModal()
                            dialog.Destroy()
        else:
            msg = ('Analysis was canceled.')
            dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
            log = open("temp.log","w")
            log.write("Error: Test was canceled")
            log.close()
            tolog = log.read()
            self.__log(tolog)
        dlg.Destroy()
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_OM_RD.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask58(self, event):
        self.__log('Batch processing ...')
        dlg = DataSets(self, -1, "Operational Model - Receptor depletion", size=(350, 200),
                       #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                       style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
                       )
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            curves = np.loadtxt('nc.tmp')
            os.remove('nc.tmp')
            if curves == 2:
                exec_full(str(install_dir)+'FR_OM_RD_a_2.py')
            else:
                if curves == 3:
                    exec_full(str(install_dir)+'FR_OM_RD_a_3.py')
                else:
                    if curves == 4:
                        exec_full(str(install_dir)+'FR_OM_RD_a_4.py')
                    else:
                        if curves == 5:
                            exec_full(str(install_dir)+'FR_OM_RD_a_5.py')
                        else:
                            msg = ('Wrong number of curves\n')
                            dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
                            dialog.ShowModal()
                            dialog.Destroy()
        else:
            msg = ('Analysis was canceled.')
            dialog = wx.MessageDialog(self, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
            log = open("temp.log","w")
            log.write("Error: Test was canceled")
            log.close()
            tolog = log.read()
            self.__log(tolog)
        dlg.Destroy()
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_OM_RD.res','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask58aa(self, event):
        self.__log('Batch processing ...')
        exec_full(str(install_dir)+'FR_OMARD_RD_a_5.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)
        log = open('FR_OMARD_RD.res','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnTask59a(self, event):
        self.__log('Interactive analysis ...')
        exec_full(str(install_dir)+'saturation_i_s.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnTask59(self, event):
        self.__log('Interactive analysis ...')
        exec_full(str(install_dir)+'saturation_i.py')
        log = open('temp.log','r')
        tolog = log.read()
        self.__log(tolog)

    def OnModel3L(self, event):
        self.__log('Modelling allosteric interaction ...')
        exec_full(str(install_dir)+'Model3L.py')
        log = open('temp.log','r')
        tolog = log.read()
        log = open('Model.def','r')
        tolog = log.read()
        self.__log(tolog)

    def OnModelOMA(self, event):
        self.__log('Modelling OMA ...')
        exec_full(str(install_dir)+'ModelOMA.py')
        log = open('temp.log','r')
        tolog = log.read()
        log = open('Model.def','r')
        tolog = log.read()
        self.__log(tolog)

    def OnModelOMAMA(self, event):
        self.__log('Modelling OMAMA ...')
        exec_full(str(install_dir)+'ModelOMAMA.py')
        log = open('temp.log','r')
        tolog = log.read()
        log = open('Model.def','r')
        tolog = log.read()
        self.__log(tolog)

    def OnModelOMAFBdelta(self, event):
        self.__log('Modelling OMA with signal feedback ...')
        exec_full(str(install_dir)+'ModelFeedBackDelta.py')
        log = open('temp.log','r')
        tolog = log.read()
        log = open('Model.def','r')
        tolog = log.read()
        self.__log(tolog)

    def OnModelOMAFBtau(self, event):
        self.__log('Modelling OMA with signal feedback ...')
        exec_full(str(install_dir)+'ModelFeedBackTau.py')
        log = open('temp.log','r')
        tolog = log.read()
        log = open('Model.def','r')
        tolog = log.read()
        self.__log(tolog)

    def OnModelOMANCIKe(self, event):
        self.__log('Modelling OMA non-competitive auto-inhibition ...')
        exec_full(str(install_dir)+'ModelOMANCIKe.py')
        log = open('temp.log','r')
        tolog = log.read()
        log = open('Model.def','r')
        tolog = log.read()
        self.__log(tolog)

    def OnModelOMANCIKi(self, event):
        self.__log('Modelling OMA non-competitive auto-inhibition ...')
        exec_full(str(install_dir)+'ModelOMANCIKi.py')
        log = open('temp.log','r')
        tolog = log.read()
        log = open('Model.def','r')
        tolog = log.read()
        self.__log(tolog)

    def OnModelOMANCIRtot(self, event):
        self.__log('Modelling OMA non-competitive auto-inhibition ...')
        exec_full(str(install_dir)+'ModelOMANCIRtot.py')
        log = open('temp.log','r')
        tolog = log.read()
        log = open('Model.def','r')
        tolog = log.read()
        self.__log(tolog)

    def OnModelOMALEK(self, event):
        self.__log('Modelling OMA of low expression system ...')
        exec_full(str(install_dir)+'ModelLowExpression_Ke.py')
        log = open('temp.log','r')
        tolog = log.read()
        log = open('Model.def','r')
        tolog = log.read()
        self.__log(tolog)

    def OnModelOMALER(self, event):
        self.__log('Modelling OMA of low expression system ...')
        exec_full(str(install_dir)+'ModelLowExpression_Rtot.py')
        log = open('temp.log','r')
        tolog = log.read()
        log = open('Model.def','r')
        tolog = log.read()
        self.__log(tolog)

    def OnModelOMARDa(self, event):
        self.__log('Modelling OMARD ...')
        exec_full(str(install_dir)+'ModelOMARDa.py')
        log = open('temp.log','r')
        tolog = log.read()
        log = open('Model.def','r')
        tolog = log.read()
        self.__log(tolog)

    def OnModelOMARDb(self, event):
        self.__log('Modelling OMARD ...')
        exec_full(str(install_dir)+'ModelOMARDb.py')
        log = open('temp.log','r')
        tolog = log.read()
        log = open('Model.def','r')
        tolog = log.read()
        self.__log(tolog)

    def OnModelOMARDr(self, event):
        self.__log('Modelling OMARD ...')
        exec_full(str(install_dir)+'ModelOMARDr.py')
        log = open('temp.log','r')
        tolog = log.read()
        log = open('Model.def','r')
        tolog = log.read()
        self.__log(tolog)

    def OnModelOMASIKe(self, event):
        self.__log('Modelling OMA substrate inhibition ...')
        exec_full(str(install_dir)+'ModelOMASIKe.py')
        log = open('temp.log','r')
        tolog = log.read()
        log = open('Model.def','r')
        tolog = log.read()
        self.__log(tolog)

    def OnModelOMASIKi(self, event):
        self.__log('Modelling OMA substrate inhibition ...')
        exec_full(str(install_dir)+'ModelOMASIKi.py')
        log = open('temp.log','r')
        tolog = log.read()
        log = open('Model.def','r')
        tolog = log.read()
        self.__log(tolog)
        
    def OnModelOMASIRtot(self, event):
        self.__log('Modelling OMA substrate inhibition ...')
        exec_full(str(install_dir)+'ModelOMASIRtot.py')
        log = open('temp.log','r')
        tolog = log.read()
        log = open('Model.def','r')
        tolog = log.read()
        self.__log(tolog)

    def OnModelView(self, event):
        cmd = ('python '+str(install_dir)+'model_viewer.py')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def OnModelPar(self, event):
        cmd = ('python '+str(install_dir)+'par_viewer.py')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        

class DataSets(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE,
            useMetal=False,
            ):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, ID, title, pos, size, style)

        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, "How many data sets do you want to analyse?")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        sampleList = ['1', '2', '3', '4', '5']
        rb = wx.RadioBox(
                self, -1, "", wx.DefaultPosition, wx.DefaultSize,
                sampleList, 5, wx.RA_SPECIFY_COLS | wx.NO_BORDER
                )
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)
        rb.SetToolTip(wx.ToolTip("Select the number"))
        sizer.Add(rb, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 20)

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
    def EvtRadioBox(self, event):
        choice = (event.GetSelection())
        curves = float(choice) + 1
        nc = open('nc.tmp','w')
        nc.write(str(curves))
        nc.close()
        
app = wx.App(False)
frame = MainWindow()
frame.Show()
app.MainLoop()
