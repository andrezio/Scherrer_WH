#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Andre
#
# Created:     04/07/2017
# Copyright:   (c) Andre 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import gauss as functions


x,y = np.loadtxt('outsampleky03111.xy', unpack= True)
x1,y1 = np.loadtxt('outstandartky03111.xy', unpack= True)

#print '### Scherrer ###'
#functions.GaussCalc(x,y,x1,y1)

#print '### Single Line ###'
#functions.VoigtCalc(x,y,x1,y1)

functions.FFT(x,y,x1,y1)
