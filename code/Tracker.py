import time, sys
from machine import Pin, PWM
from StepperMotor import StepperMotor as Motor
from config import *


class Tracker:
    def __init__(self):
        self.led1 = Pin(PIN_LED_1, Pin.OUT)
        self.led2 = Pin(PIN_LED_2, Pin.OUT)
        self.led3 = Pin(PIN_LED_3, Pin.OUT)
        self.buzzer = PWM(Pin(PIN_BUZZER))
        self.buzzer.freq(3000)
        self.buzzer.duty_u16(0)

        self.ma = Motor(PIN_M1_ENABLE, PIN_M1_STEP, PIN_M1_DIR)
        self.mb = Motor(PIN_M2_ENABLE, PIN_M2_STEP, PIN_M2_DIR)
        self.mc = Motor(PIN_M3_ENABLE, PIN_M3_STEP, PIN_M3_DIR)
        self.ma.enable()
        self.mb.enable()
        self.mc.enable()
        
        self.pos_a = 0
        self.pos_b = 0
        self.pos_c = 0
        
    def moveTo(self, dest_a, dest_b, dest_c):
        self.bresenham3D(dest_a, dest_b, dest_c)
        
        
    def bresenham3D(self, dest_a, dest_b, dest_c):
        da = abs(dest_a - self.pos_a)
        db = abs(dest_b - self.pos_b)
        dc = abs(dest_c - self.pos_c)
        
        print('da: ', da, 'db: ', db, 'dc: ', dc)
        
        dir_a = 1 if dest_a > self.pos_a else -1
        dir_b = 1 if dest_b > self.pos_b else -1
        dir_c = 1 if dest_c > self.pos_c else -1
        print('dira: ', dir_a, ' dirb: ', dir_b, ' dirc: ', dir_c)
        
        temp_a = 0
        temp_b = 0
        temp_c = 0
        if not (da == 0 and db == 0 and dc == 0):
            if da >= db and da >= dc:
                step_b = db / da
                step_c = dc / da

                for x in range(da):
                    self.pos_a = self.pos_a + dir_a
                    self.ma.step(dir_a)
                    temp_b = temp_b + step_b
                    temp_c = temp_c + step_c
                    
                    if temp_b >= 1:
                        temp_b = temp_b - 1
                        self.pos_b = self.pos_b + dir_b
                        self.mb.step(dir_b)

                    if temp_c >= 1:
                        temp_c = temp_c - 1
                        self.pos_c = self.pos_c + dir_c
                        self.mc.step(dir_c)
                    time.sleep(DELAY_BETWEEN_STEPS)
                    #print(self.pos_a, self.pos_b, self.pos_c)
                    
            elif db >= da and db >= dc:
                step_a = da / db
                step_c = dc / db

                for x in range(db):
                    self.pos_b = self.pos_b + dir_b
                    self.mb.step(dir_b)
                    temp_a = temp_a + step_a
                    temp_c = temp_c + step_c
                    
                    if temp_a >= 1:
                        temp_a = temp_a - 1
                        self.pos_a = self.pos_a + dir_a
                        self.ma.step(dir_a)

                    if temp_c >= 1:
                        temp_c = temp_c - 1
                        self.pos_c = self.pos_c + dir_c
                        self.mc.step(dir_c)
                    time.sleep(DELAY_BETWEEN_STEPS)
                    print(self.pos_a, self.pos_b, self.pos_c)

            elif dc >= da and dc >= db:
                step_a = da / dc
                step_b = db / dc

                for x in range(dc):
                    self.pos_c = self.pos_c + dir_c
                    self.mc.step(dir_c)
                    temp_a = temp_a + step_a
                    temp_b = temp_b + step_b
                    
                    if temp_a >= 1:
                        temp_a = temp_a - 1
                        self.pos_a = self.pos_a + dir_a
                        self.ma.step(dir_a)

                    if temp_b >= 1:
                        temp_b = temp_b - 1
                        self.pos_b = self.pos_b + dir_b
                        self.mb.step(dir_b)
                    time.sleep(DELAY_BETWEEN_STEPS)
                    print(self.pos_a, self.pos_b, self.pos_c)
                
    def getA(self):
        return self.pos_a
    
    def getB(self):
        return self.pos_b
    
    def getC(self):
        return self.pos_c
                
                
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
