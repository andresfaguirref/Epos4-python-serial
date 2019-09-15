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

ANG = input('Ingrese angulo en grados: ')

Steps_Motor = 4096
Steps_Exo = 160
decode = Decode_Ang_MotorStep.Decode_Angle_MotorSteps(Steps_Motor*4,Steps_Exo)

#Motor = SerialEpos4.SerialEpos4('COM24',"\x02")
#Motor.OpenPort()
#Motor.Enable_to_move()
Step = decode.Decode_Angle2StepMotor(ANG)
print(Step)
#Motor.Move_position(int(Step))

