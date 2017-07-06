#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Andre
#
# Created:     03/07/2017
# Copyright:   (c) Andre 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from lmfit.models import VoigtModel, GaussianModel
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.signal import savgol_filter


def savitzgolay_filter(y,w=51,p=9):
    return savgol_filter(y,w,p)

def ScherrerEquation(sigma,center):
    lambida=0.1033305

    center=np.cos(np.radians(center/2))

    D=(0.9*lambida)/(2.3548*sigma*center)

    print 'D:', int(D), 'nm'

def GaussCalc(x,y,x1,y1):

    y=removerBackground(y)
    y1=removerBackground(y1)

    mod = GaussianModel()
    pars = mod.guess(y, x=x)
    out  = mod.fit(y, pars, x=x)


    mod = GaussianModel()
    pars1 = mod.guess(y1, x=x1)
    out1  = mod.fit(y1, pars1, x=x1)


    center=out.best_values['center']


    sigma = Decon_Gau(out.best_values['sigma'],out1.best_values['sigma']) 

    return ScherrerEquation(sigma, center)

def SingleLineEquation(sigma, gamma, center):
    lambida=0.1033305

    tancenter=np.tan(np.radians(center/2))

    center=np.cos(np.radians(center/2))

    D=(1.0*lambida)/(2*gamma*(np.pi/2)*center)

    e=2.3548*sigma*(1.06446701943)/(tancenter*4)

    #e=e*(2/np.pi)

    print 'D:', int(D), ' nm'
    print '<e>:',round(e,3)

def VoigtCalc(x,y,x1,y1):
    y=removerBackground(y)
    y1=removerBackground(y1)

    mod = VoigtModel()
    pars = mod.guess(y, x=x)
    pars['gamma'].set(value=0.7, vary=True, expr='')
    out  = mod.fit(y, pars, x=x)


    mod = VoigtModel()
    pars1 = mod.guess(y1, x=x1)
    pars1['gamma'].set(value=0.7, vary=True, expr='')
    out1  = mod.fit(y1, pars1, x=x1)


    center=out.best_values['center']

    sigma = Decon_Gau(out.best_values['sigma'],out1.best_values['sigma'])   

    gamma = Decon_Lor(out.best_values['gamma'],out1.best_values['gamma'])

    return SingleLineEquation(sigma, gamma, center)

def removerBackground(y,n=8):

    minimo = min(y)
    for i in range(len(y)):
        y[i]-=minimo
        if i <=n or i>=(len(y)-n):
            y[i]=0.0

    return y

def Plotar(x,y,x2,y2):

    plt.figure(1)
    plt.plot(x,y,'-o',label='sample')
    plt.plot(x2,y2 , '-o',label='std')
    plt.legend()
    plt.grid()
    plt.show()

def Decon_Lor(s1,s2):
    return np.radians(s1-s2)

def Decon_Gau(s1,s2):
    return np.radians(np.sqrt(pow(s1,2)-pow(s2,2)))



def deconvolution(y,y1):
    newy=[]

    for i in range(len(y)):
        try:
            newy.append(y[i].real/y1[i].real)
        except:
            pass

    return newy

def FFT(x,y,x1,y1):
    y=np.fft.rfft(y)
    y1=np.fft.rfft(y1)

    yy=deconvolution(y,y1)

    plt.plot(yy,'-o')
    plt.show()

