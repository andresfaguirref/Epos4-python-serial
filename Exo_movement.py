from __future__ import division
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import samplerate

import serial, time
import crc16

import CalculatedAngles
import Decode_Ang_MotorStep

import SerialEpos4

Movement='Kicks'
Sampling_Frequency=500
M=(CalculatedAngles.AnglesJoint(Movement,Sampling_Frequency))
M = M*180/np.pi
Hip = M[0,:].T
Knee = M[1,:].T
Ankle = M[2,:].T

Hip_res = []
Knee_res = []
Ankle_res = []
for x in range (0,len(Hip)):
    if x == 0:
        Hip_res.append(Hip[x,0])
        Knee_res.append(Knee[x,0])
        Ankle_res.append(Ankle[x,0])
    else:
        Hip_res.append(Hip[x,0] - Hip[x-1,0])
        Knee_res.append(Knee[x,0] - Knee[x-1,0])
        Ankle_res.append(Ankle[x,0] - Ankle[x-1,0])

Steps_Motor = 4096
Steps_Exo = 160
decode = Decode_Ang_MotorStep.Decode_Angle_MotorSteps(Steps_Motor*4,Steps_Exo)

#Motor_Hip = SerialEpos4.SerialEpos4('COM24',"\x02")
#Motor_Hip.OpenPort()
#Motor_Hip.Enable_to_move()

#Motor_Knee = SerialEpos4.SerialEpos4('COM24',"\x02")
#Motor_Knee.OpenPort()
ti = input('% de vel: ')
TT = (1/10)*(100/ti) 
x = 0
p=1
ini = 0

while True :
    if x >= len(Hip)-1:
        p=-1
        print('FIN')
    
    if x==0:
        ang = Hip[x,0] - ini
        ini = Hip[x,0]
        Step = decode.Decode_Angle2StepMotor(ang)
        print('Step: ' + str(Step))
        print('Angle: ' + str(ang))
        print('INCIO')
        #Motor_Hip.Move_position(int(Step))
        time.sleep(1/10)
        x = x+p
        p=1
    elif x%50 == 0:
        ang = Hip[x,0] - ini
        ini = Hip[x,0]
        Step = decode.Decode_Angle2StepMotor(ang)
        #Motor_Hip.Move_position(int(Step))
        time.sleep(1/10)
        print('Step: ' + str(Step))
        print('Angle: ' + str(ang))
        x = x+p
    else:
        x = x+p

    
Motor_Hip.Disenable_to_move()
