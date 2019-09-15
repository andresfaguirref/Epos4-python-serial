from __future__ import division
class Decode_Angle_MotorSteps(object):
    def __init__(self,Steps_Motor,Steps_Exo):
        self.Steps_Motor = Steps_Motor
        self.Steps_Exo= Steps_Exo
        self.factor = (360/Steps_Exo)

    def Decode_Angle2StepMotor(self,Angle):
        return (self.Steps_Motor)*(Angle/self.factor)
