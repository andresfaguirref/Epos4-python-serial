from __future__ import division
import numpy as np
import CalculatedAngles
import Decode_Ang_MotorStep

import SerialEpos4

import serial, time
import crc16

Motor_Knee = SerialEpos4.SerialEpos4('COM21',"\x01")
Motor_Knee.OpenPort()
Motor_Knee.Enable_to_move()

Demand_Angle = 0
t=0.01
Ext_limit = 0
Fle_limit = -50
Interval = 1
status = 'UP'

Steps_Motor = 4096
Steps_Exo = 160
decode = Decode_Ang_MotorStep.Decode_Angle_MotorSteps(Steps_Motor*4,Steps_Exo)


while True :

    if Demand_Angle >= Ext_limit:
        #print ('')
        status = 'DOWN'
        #print (status)
        #print ('')
        
    elif Demand_Angle <= Fle_limit:
        #print ('')
        status = 'UP'
        #print (status)
        #print ('')
        
        

    if  status == 'DOWN':

        Demand_Angle = Demand_Angle - Interval
        Step = decode.Decode_Angle2StepMotor(-1*Interval)
        Motor_Knee.Move_position(int(Step))
        print('Angle: ' + str(Demand_Angle))
        print('Step: ' + str(Step))
        time.sleep(t)
        
    
    elif status == 'UP':
        Demand_Angle = Demand_Angle + Interval
        Step = decode.Decode_Angle2StepMotor(Interval)
        Motor_Knee.Move_position(int(Step))
        print('Angle: ' + str(Demand_Angle))
        print('Step: ' + str(Step))
        time.sleep(t)
        
    else:
        print('Nothing')

    
Motor_Knee.Disenable_to_move()
Motor_Knee.ClosePort()
