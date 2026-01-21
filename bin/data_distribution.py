#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:35:07 2016

@author: Jan Jakubik jan.jakubik@fgu.cas.cz
"""
import glob,os
import time
import wx
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skewtest
from scipy.stats import kurtosistest

#color list
color_list = np.array(['k','b','r','g','c','m','y'])

#error log
if os.path.isfile("temp.log"):
    os.remove("temp.log")
err = ''

#initialize counters
i = -1
x_max_max = 0
y_max_max = 0

#test wheter we have files
count = len(glob.glob('*.dat'))
if count == 0:
    msg = ('No .dat files found!\n')
    err = msg
    dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
else:
    #prepare file for writing results
    if os.path.isfile("data_distribution.res"):
        os.remove("data_distribution.res")
    res = open("data_distribution.res","w")
    res.write("Data distgribution analysis\n\n")
    res.write("Skewness\tP-value\tKurtosis\tP-value\tData file\n")
    #prepare file for Grace plot
    if os.path.isfile("data_dist.draw"):
        os.remove("data_dist.draw")
    draw = open("data_dist.draw","w")
    c=-1 #plot counter
    d=0 #symbolcounter
    
    for file in sorted(glob.glob('*.dat')):
        if file == '':
          exit()
        # load data
        x_data = np.loadtxt(file)
        if np.size(x_data) < 100:
            msg = ('Too few data points in ' +str(file)+ ' This data will be skipped\n')
            err = err + msg
            dialog = wx.MessageDialog(None, msg, 'Error', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            #analyze data
            s, ps = skewtest(x_data)
            k, pk = kurtosistest(x_data)
            #write results
            results = (str("{0:.4f}".format(s))+"\t"+str("{0:.4f}".format(ps))+"\t"+str("{0:.4f}".format(k))+"\t"+str("{0:.4f}".format(pk))+"\t"+str(file))
            res.write(str(results)+"\n")
            base=os.path.splitext(file)[0]
            #get color
            i = i + 1
            if i == 7:
                msg = ("More than 7 data sets. Colors repeat.\n")
                err = err + msg
                dialog = wx.MessageDialog(None, msg, 'Warning', wx.OK)
                dialog.ShowModal()
                dialog.Destroy()
                i = i - 7
            color = (color_list[i])
            # plot
            n, bins, patches = plt.hist(x_data, 20, facecolor = color)
            #calculate curve
            first_centre = ((bins[0]+bins[1])/2)
            bin_centres = np.array(first_centre)
            end = np.size(bins) - 1
            for j in range(1, end):
                centre=((bins[j]+bins[j+1])/2)
                bin_centres=np.append(bin_centres,centre)
            x_calc = bin_centres
            y_calc = n
            xy_calc = np.column_stack((x_calc, y_calc))
            #save fit curve
            fit=(str(base)+'_data_dist_fit.data')
            #write Grace plot
            c=(c+1)
            d=(d+1)
            draw.write("read xy \""+str(fit)+"\" \n")
            draw.write("s"+str(c)+" symbol 0 \n")
            draw.write("s"+str(c)+" line type 2 \n")
            draw.write("s"+str(c)+" line color "+str(d)+" \n")
            draw.write("s"+str(c)+" layer 50 \n")
            draw.write("s"+str(c)+" legend \" skew = "+str("{0:.4f}".format(s))+"  P = "+str("{0:.4f}".format(ps))+"  kurt = "+str("{0:.4f}".format(k))+"  P = "+str("{0:.4f}".format(pk))+"\\n "+str(file)+"\" \n")
            np.savetxt(fit,xy_calc,fmt='%.4e')
    
    now = time.strftime("%d.%m.%Y %H:%M:%S")
    res.write("\n\n"+str(now)+"\n")
    res.close()
    #Plot
    plt.title("Data distribution")
    plt.xlabel("bins")
    plt.ylabel("n")
    plt.show()
    #Grace plot
    draw.write("page size 595, 842 \n")
    draw.write("view xmin 0.2 \n")
    draw.write("view xmax 0.8 \n")
    draw.write("view ymin 0.85 \n")
    draw.write("view ymax 1.25 \n")
    draw.write("xaxis label \"Bins\"  \n")
    draw.write("xaxis label font \"Helvetica\"  \n")
    draw.write("xaxis ticklabel font \"Helvetica\"  \n")
    draw.write("xaxis  tick major size 0.8 \n")
    draw.write("xaxis  tick minor size 0.4 \n")
    draw.write("yaxis label \"N\"  \n")
    draw.write("yaxis label font \"Helvetica\"  \n")
    draw.write("yaxis ticklabel font \"Helvetica\"  \n")
    draw.write("yaxis  tick major size 0.8 \n")
    draw.write("yaxis  tick minor size 0.4 \n")
    draw.write("legend 0.08, 0.7 \n")
    draw.write("legend char size 0.8 \n")
    draw.write("legend font \"Helvetica\" \n")
    draw.close()

log = open("temp.log","w")
log.write(err)
log.close()
