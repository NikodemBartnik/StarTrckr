import pygame, math, time, gui
import serial

pygame.init()
screen = pygame.display.set_mode([800, 400])

SERIALPORT ='/dev/cu.usbserial-1410'
#tracker = Serial(SERIALPORT, 115200, timeout=0.01)

mousePressed = False


def clickCheck(pos, clicked):
    joystick.checkIfPressed(pos, clicked)
    button_turn_left.checkIfPressed(pos, clicked)
    button_turn_right.checkIfPressed(pos, clicked)
    button_set_axis.checkIfPressed(pos, clicked)
    button_track.checkIfPressed(pos, clicked)

def drawAll():
    joystick.draw(screen)
    button_turn_left.draw(screen)
    button_turn_right.draw(screen)
    title_turn.draw(screen)
    titleL.draw(screen)
    titleR.draw(screen)
    title_set_axis.draw(screen)
    button_set_axis.draw(screen)
    title_track.draw(screen)
    button_track.draw(screen)
    title_angle.draw(screen)

joystick = gui.Joystick((260,200), 120)
title_turn = gui.Title((590,60), 'Turn')
titleL = gui.Title((545,120), 'L')
titleR = gui.Title((675,120), 'R')
button_turn_left = gui.Button((550, 130), 30, False, False)
button_turn_right = gui.Button((680, 130), 30, False, False)
title_set_axis = gui.Title((520, 210), 'Set axis')
button_set_axis = gui.Button((650, 220), 20, False, False)
title_track = gui.Title((520, 280), 'Track')
button_track = gui.Button((650, 290), 20, False, True)
title_angle = gui.Title((580, 340), 'set axis')

def WaitForOK():
    while(1):
        if(tracker.readline() == b'OK\n'):
            break


angle_a = 0
angle_b = 0
angle_c = 0

while 1:
    screen.fill((40,40,40))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            mousePressed = False
        if event.type == pygame.QUIT:
            pygame.quit()
        clickCheck(pygame.mouse.get_pos(), mousePressed)
        
    drawAll()
    a = joystick.getValue()
    if a[0] > 50 and a[0] < 130 and a[1] > 0.5:
        angle_c = angle_c + 0.2
    if a[0] > 230 and a[0] < 310 and a[1] > 0.5:
        angle_c = angle_c - 0.2

    if a[0] > 140 and a[0] < 210 and a[1] > 0.5:
        angle_a = angle_a + 0.2
    if a[0] > 320 or a[0] < 40 and a[1] > 0.5:
        angle_a = angle_a - 0.2

    if button_turn_right.getValue():
        angle_b = angle_b + 0.2
    if button_turn_left.getValue():
        angle_b = angle_b - 0.2

    
    print('A', round(angle_a, 2), ' B', round(angle_b, 2), ' C', round(angle_c, 2))
    time.sleep(0.01)
    pygame.display.flip()