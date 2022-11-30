import time, sys
from machine import Pin, PWM
from StepperMotor import StepperMotor as Motor
from config import *
from Tracker import Tracker as Tracker

    
def readCommand():
    global pos_a, pos_b, pos_c
    cm_list = sys.stdin.readline().strip().split(' ')
    print(cm_list)
    if cm_list[0] != '':
        targets = [tracker.getA(), tracker.getB(), tracker.getC()]
        if len(cm_list) >= 1:
            if cm_list[0][0] == 'A':
                print('Moving A axis by: ', int(cm_list[0][1:]), ' deg\n')
                targets[0] = int(cm_list[0][1:]) * A_STEPS_PER_DEGREE
                
        if len(cm_list) >= 2:
            if cm_list[1][0] == 'B':
                print('Moving B axis by: ', int(cm_list[1][1:]), ' deg\n')
                targets[1] = int(cm_list[1][1:]) * B_STEPS_PER_DEGREE
        if len(cm_list) >= 3:
            if cm_list[2][0] == 'C':
                print('Moving C axis by: ', int(cm_list[2][1:]), ' deg\n')
                targets[2] = int(cm_list[2][1:]) * C_STEPS_PER_DEGREE
                
        tracker.moveTo(targets[0], targets[1], targets[2])
        

tracker = Tracker()
while(1):
    readCommand()