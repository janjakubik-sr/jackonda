#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 12:54:35 2026

@author: roshi
"""

import glob,os
import wx

def add_zero_column(input_file, output_file):
    try:
        with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
            for line_num, line in enumerate(f_in, 1):
                parts = line.split()
                
                # Skip empty lines silently
                if not parts:
                    continue
                
                # Validation: Check for exactly 2 columns
                if len(parts) == 2:
                    parts.append('0')
                    f_out.write(" ".join(parts) + "\n")
                else:
                    print(f"Skipping line {line_num}: Expected 2 columns, found {len(parts)}.")
                    
        print(f"\nProcessing complete. Check '{output_file}' for results.")
        
    except FileNotFoundError:
        print("Error: The input file was not found.")

#error log
if os.path.isfile("temp.log"):
    os.remove("temp.log")
log = open("temp.log","w")

#test wheter we have files
count = len(glob.glob('*.dat'))
if count == 0:
    msg = ('No .dat files found!\n')
    err = msg
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
else:
    for file in sorted(glob.glob('*.dat')):
        if file == '':
            exit()
        base=os.path.splitext(file)[0]
        file_out=(str(base)+"_out.dat")
        add_zero_column(file, file_out)

log.close()
    