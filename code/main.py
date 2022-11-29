import time, sys
from machine import Pin, PWM
from StepperMotor import StepperMotor as Motor

led1 = Pin(6, Pin.OUT)
led2 = Pin(7, Pin.OUT)
led3 = Pin(8, Pin.OUT)
#buzzer = PWM(Pin(9))
#buzzer.freq(3000)
#buzzer.duty_u16(30000)

m1 = Motor(24, 23, 22)
m2 = Motor(21, 20, 19)
m3 = Motor(18, 17, 16)

A_STEPS_PER_DEGREE = 35
B_STEPS_PER_DEGREE = 35
C_STEPS_PER_DEGREE = 35

a_pos = 0
b_pos = 0
c_pos = 0

def buzzerSound():
    buzzer.duty_u16(30000)
    time.sleep(0.1)
    buzzer.duty_u16(0)
    time.sleep(0.5)
    buzzer.duty_u16(30000)
    time.sleep(0.1)
    buzzer.duty_u16(0)
    time.sleep(0.5)
    buzzer.duty_u16(30000)
    time.sleep(0.1)
    buzzer.duty_u16(0)
    time.sleep(3)
    

def comm():
    print('hello')
    v = sys.stdin.readline().strip()
    v.split(' ')
    print(v)
    time.sleep(1)
    
    
def readCommand():
    cm_list = sys.stdin.readline().strip().split(' ')
    print(cm_list)
    if cm_list[0] != '':
        if len(cm_list) >= 1:
            if cm_list[0][0] == 'A':
                print('Moving A axis by: ', int(cm_list[0][1:]), ' deg\n')
                moveTo(0, int(cm_list[0][1:]))
                
        if len(cm_list) >= 2:
            if cm_list[1][0] == 'B':
                print('Moving B axis by: ', int(cm_list[1][1:]), ' deg\n')
                moveTo(1, int(cm_list[1][1:]))
        if len(cm_list) >= 3:
            if cm_list[2][0] == 'C':
                print('Moving C axis by: ', int(cm_list[2][1:]), ' deg\n')
                moveTo(2, int(cm_list[2][1:]))
        
        
def moveTo(axis, degrees):
    global a_pos, b_pos, c_pos
    if axis == 0:
        steps_to_do = (degrees - a_pos) * A_STEPS_PER_DEGREE
        for x in range(abs(steps_to_do)):
            m1.step(1 if steps_to_do > 0 else 0)
            time.sleep(0.003)
        a_pos = degrees
    elif axis == 1:
        steps_to_do = (degrees - b_pos) * B_STEPS_PER_DEGREE
        for x in range(abs(steps_to_do)):
            m2.step(1 if steps_to_do > 0 else 0)
            time.sleep(0.002)
        b_pos = degrees
    elif axis == 2:
        steps_to_do = (degrees - c_pos) * C_STEPS_PER_DEGREE
        for x in range(abs(steps_to_do)):
            m3.step(1 if steps_to_do > 0 else 0)
            print(x)
            time.sleep(0.002)
        c_pos = degrees
        
def bresenham3D(curr_a, curr_b, curr_c, dest_a, dest_b, dest_c):
    da = abs(dest_a - curr_a)
    db = abs(dest_b - curr_b)
    dc = abs(dest_c - curr_c)
    
    dir_a = 1 if dest_a > curr_a else -1
    dir_b = 1 if dest_b > curr_b else -1
    dir_c = 1 if dest_c > curr_c else -1
    
    if da >= db and da >= dc:
        pass
    elif db >= da and db >= dc:
        pass
    elif dc >= da and dc >= db:
        pass
    


#temp_dir = 1
m1.enable()
m2.enable()
m3.enable()
# temp_dir = 0 if temp_dir else 1
#     print(temp_dir)
#     led1.toggle()
#     for i in range(2000):
#         m1.step(temp_dir)
#         m2.step(temp_dir)
#         m3.step(temp_dir)
#         time.sleep(0.003)    

#m1.disable()
#m2.disable()
#m3.disable()
while(1):
    readCommand()
        
    

