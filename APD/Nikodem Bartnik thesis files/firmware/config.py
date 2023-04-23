PIN_LED_1 = 6
PIN_LED_2 = 7
PIN_LED_3 = 8
PIN_BUZZER = 9
PIN_M1_ENABLE = 24
PIN_M1_STEP = 23
PIN_M1_DIR = 22
PIN_M2_ENABLE = 21
PIN_M2_STEP = 20
PIN_M2_DIR = 19
PIN_M3_ENABLE = 18
PIN_M3_STEP = 17
PIN_M3_DIR = 16

M1_REVERSE_DIR = False
M2_REVERSE_DIR = True
M3_REVERSE_DIR = True

#small base gear: 10 teeth
#big base gear: 50 teeth
#motor steps: 200 steps/rev
#microstepping: 1/16
#result: 16 000 steps/rev so 44.44 steps per degree
A_STEPS_PER_DEGREE = 44
#small pulley: 16 teeth
#big pulley: 70 teeth
#motor steps: 200 steps/rev
#microstepping: 1/16
#result: 14 000 steps/rev so 38.89 steps per degree
B_STEPS_PER_DEGREE = 39
C_STEPS_PER_DEGREE = 39

DELAY_BETWEEN_STEPS = 0.002