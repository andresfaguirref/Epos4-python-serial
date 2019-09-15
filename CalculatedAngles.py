# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 06:24:33 2017

@author: Nathalia
"""

import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import samplerate

def AnglesJoint(Movement,Sampling_Frequency):
    fs=500
    if Movement=='Straight Walking':
        ## Choose the files corresponding with the parameter
        ##movement
        #Knee
        AngRK= open('Angle_RightKnee_WS.txt')
        AngRK=AngRK.read().split()
        AngRK=np.array(AngRK)
        AngRK=AngRK.astype(float)
        ##Hip
        AngRH= open('Angle_RightHip_WS.txt')
        AngRH=AngRH.read().split()
        AngRH=np.array(AngRH)
        AngRH=AngRH.astype(float)
        ##Ankle
        AngRA= open('Angle_RightAnkle_WS.txt')
        AngRA=AngRA.read().split()
        AngRA=np.array(AngRA)
        AngRA=AngRA.astype(float)
    elif Movement=='Straight Running':
        #Knee
        AngRK= open('Angle_RightKnee_RS.txt')
        AngRK=AngRK.read().split()
        AngRK=np.array(AngRK)
        AngRK=AngRK.astype(float)
        ##Hip
        AngRH= open('Angle_RightHip_RS.txt')
        AngRH=AngRH.read().split()
        AngRH=np.array(AngRH)
        AngRH=AngRH.astype(float)
        ##Ankle
        AngRA= open('Angle_RightAnkle_RS.txt')
        AngRA=AngRA.read().split()
        AngRA=np.array(AngRA)
        AngRA=AngRA.astype(float)
    elif Movement== 'Avoiding obstacles':
        #Knee
        AngRK= open('Angle_RightKnee_AO.txt')
        AngRK=AngRK.read().split()
        AngRK=np.array(AngRK)
        AngRK=AngRK.astype(float)
        ##Hip
        AngRH= open('Angle_RightHip_AO.txt')
        AngRH=AngRH.read().split()
        AngRH=np.array(AngRH)
        AngRH=AngRH.astype(float)
        ##Ankle
        AngRA= open('Angle_RightAnkle_AO.txt')
        AngRA=AngRA.read().split()
        AngRA=np.array(AngRA)
        AngRA=AngRA.astype(float)
    elif Movement== 'Squats':
        #Knee
        AngRK= open('Angle_RightKnee_Sq.txt')
        AngRK=AngRK.read().split()
        AngRK=np.array(AngRK)
        AngRK=AngRK.astype(float)
        ##Hip
        AngRH= open('Angle_RightHip_Sq.txt')
        AngRH=AngRH.read().split()
        AngRH=np.array(AngRH)
        AngRH=AngRH.astype(float)
        ##Ankle
        AngRA= open('Angle_RightAnkle_Sq.txt')
        AngRA=AngRA.read().split()
        AngRA=np.array(AngRA)
        AngRA=AngRA.astype(float)
    elif Movement=='Kicks':
        #Knee
        AngRK= open('Angle_RightKnee_K.txt')
        AngRK=AngRK.read().split()
        AngRK=np.array(AngRK)
        AngRK=AngRK.astype(float)
        ##Hip
        AngRH= open('Angle_RightHip_K.txt')
        AngRH=AngRH.read().split()
        AngRH=np.array(AngRH)
        AngRH=AngRH.astype(float)
        ##Ankle
        AngRA= open('Angle_RightAnkle_K.txt')
        AngRA=AngRA.read().split()
        AngRA=np.array(AngRA)
        AngRA=AngRA.astype(float)
    elif Movement== 'Jump':
        #Knee
        AngRK= open('Angle_RightKnee_J.txt')
        AngRK=AngRK.read().split()
        AngRK=np.array(AngRK)
        AngRK=AngRK.astype(float)
        ##Hip
        AngRH= open('Angle_RightHip_J.txt')
        AngRH=AngRH.read().split()
        AngRH=np.array(AngRH)
        AngRH=AngRH.astype(float)
        ##Ankle
        AngRA= open('Angle_RightAnkle_J.txt')
        AngRA=AngRA.read().split()
        AngRA=np.array(AngRA)
        AngRA=AngRA.astype(float)
    #Return parameters 
    # Simple API
    ratio = float(Sampling_Frequency)/float(fs)
    print(ratio)
    converter = 'sinc_best'  # or 'sinc_fastest', ...
    AngRK_m = samplerate.resample(AngRK, ratio, converter)
    AngRH_m = samplerate.resample(AngRH, ratio, converter)
    AngRA_m = samplerate.resample(AngRA, ratio, converter)
    Angles= np.matrix([AngRH_m,AngRK_m,AngRA_m])
    return (Angles)
    

#Call function 
#Movement='Kicks'
#Sampling_Frequency=500
#M=(AnglesJoint(Movement,Sampling_Frequency))
#figure(1)
#plt.plot(M[0,:].T)



        
        
        
    
        
    


