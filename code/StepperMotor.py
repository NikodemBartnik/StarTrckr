from machine import Pin

class StepperMotor:
    def __init__(self, pin_enable, pin_step, pin_dir):
        self.pin_dir = Pin(pin_dir, Pin.OUT)
        self.pin_step = Pin(pin_step, Pin.OUT)
        self.pin_enable = Pin(pin_enable, Pin.OUT)
        
    def enable(self):
        self.pin_enable.value(0)
        
    def disable(self):
        self.pin_enable.value(1)
        
    def step(self, direction):
        self.pin_dir.value(1) if direction == 1 else self.pin_dir.value(0)
        self.pin_step.value(1)
        self.pin_step.value(0)
        
        
    