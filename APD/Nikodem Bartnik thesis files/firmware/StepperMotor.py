from machine import Pin

class StepperMotor:
    def __init__(self, pin_enable, pin_step, pin_dir, reverse_dir):
        self.pin_dir = Pin(pin_dir, Pin.OUT)
        self.pin_step = Pin(pin_step, Pin.OUT)
        self.pin_enable = Pin(pin_enable, Pin.OUT)
        self.reverse_dir = reverse_dir
        
    def enable(self):
        self.pin_enable.value(0)
        
    def disable(self):
        self.pin_enable.value(1)
        
    def step(self, direction):
        self.pin_dir.value(self.reverse_dir) if direction == 1 else self.pin_dir.value(not self.reverse_dir)
        print('DIR POS') if direction == 1 else print('DIR NEG')
        self.pin_step.value(1)
        self.pin_step.value(0)
        