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

pos_a = 0
pos_b = 0
pos_c = 0

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
    
    
def readCommand(m1, m2, m3):
    global pos_a, pos_b, pos_c
    cm_list = sys.stdin.readline().strip().split(' ')
    print(cm_list)
    if cm_list[0] != '':
        targets = [pos_a, pos_b, pos_c]
        if len(cm_list) >= 1:
            if cm_list[0][0] == 'A':
                print('Moving A axis by: ', int(cm_list[0][1:]), ' deg\n')
                targets[0] = int(cm_list[0][1:])
                
        if len(cm_list) >= 2:
            if cm_list[1][0] == 'B':
                print('Moving B axis by: ', int(cm_list[1][1:]), ' deg\n')
                targets[1] = int(cm_list[1][1:])
        if len(cm_list) >= 3:
            if cm_list[2][0] == 'C':
                print('Moving C axis by: ', int(cm_list[2][1:]), ' deg\n')
                targets[2] = int(cm_list[2][1:])
                
        bresenham3D(targets[0] * A_STEPS_PER_DEGREE, targets[1] * B_STEPS_PER_DEGREE, targets[2] * C_STEPS_PER_DEGREE, m1, m2, m3)
        
        
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
        
        
def bresenham3D(dest_a, dest_b, dest_c, ma, mb, mc):
    global pos_a, pos_b, pos_c
    da = abs(dest_a - pos_a)
    db = abs(dest_b - pos_b)
    dc = abs(dest_c - pos_c)
    
    print('da: ', da, 'db: ', db, 'dc: ', dc)
    
    dir_a = 1 if dest_a > pos_a else -1
    dir_b = 1 if dest_b > pos_b else -1
    dir_c = 1 if dest_c > pos_c else -1
    print('dira: ', dir_a, ' dirb: ', dir_b, ' dirc: ', dir_c)
    
    temp_a = 0
    temp_b = 0
    temp_c = 0
    if not (da == 0 and db == 0 and dc == 0):
        if da >= db and da >= dc:
            step_b = db / da
            step_c = dc / da

            for x in range(da):
                pos_a = pos_a + dir_a
                ma.step(dir_a)
                temp_b = temp_b + step_b
                temp_c = temp_c + step_c
                
                if temp_b >= 1:
                    temp_b = temp_b - 1
                    pos_b = pos_b + dir_b
                    mb.step(dir_b)

                if temp_c >= 1:
                    temp_c = temp_c - 1
                    pos_c = pos_c + dir_c
                    mc.step(dir_c)
                time.sleep(0.005)
                print(pos_a, pos_b, pos_c)
                
        elif db >= da and db >= dc:
            step_a = da / db
            step_c = dc / db

            for x in range(db):
                pos_b = pos_b + dir_b
                mb.step(dir_b)
                temp_a = temp_a + step_a
                temp_c = temp_c + step_c
                
                if temp_a >= 1:
                    temp_a = temp_a - 1
                    pos_a = pos_a + dir_a
                    ma.step(dir_a)

                if temp_c >= 1:
                    temp_c = temp_c - 1
                    pos_c = pos_c + dir_c
                    mc.step(dir_c)
                time.sleep(0.005)
                print(pos_a, pos_b, pos_c)

        elif dc >= da and dc >= db:
            step_a = da / dc
            step_b = db / dc

            for x in range(dc):
                pos_c = pos_c + dir_c
                mc.step(dir_c)
                temp_a = temp_a + step_a
                temp_b = temp_b + step_b
                
                if temp_a >= 1:
                    temp_a = temp_a - 1
                    pos_a = pos_a + dir_a
                    ma.step(dir_a)

                if temp_b >= 1:
                    temp_b = temp_b - 1
                    pos_b = pos_b + dir_b
                    mb.step(dir_b)
                time.sleep(0.005)
                print(pos_a, pos_b, pos_c)


    


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
    readCommand(m1, m2, m3)
        
    

