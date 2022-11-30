import pygame, math, time, gui
import serial
import numpy as np

pygame.init()
screen = pygame.display.set_mode([800, 400])

SERIALPORT ='/dev/cu.usbmodem14101'
tracker = serial.Serial(SERIALPORT, 115200, timeout=0.01)

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


def WaitForOK():
    while(1):
        if(tracker.readline() == b'OK\n'):
            break


def rotateNormal(vector, angle_x, angle_y, angle_z):
    a = np.pi/180 * angle_x
    b = np.pi/180 * angle_y
    c = np.pi/180 * angle_z
    rotation_matrix = np.array([[np.cos(b)*np.cos(c), np.sin(a)*np.sin(b)*np.cos(c), np.cos(a)*np.sin(b)*np.cos(c)+np.sin(a)*np.sin(c)],
                            [np.cos(b)*np.sin(c), np.sin(a)*np.sin(b)*np.sin(c)+np.cos(a)*np.cos(c), np.cos(a)*np.sin(b)*np.sin(c)-np.sin(a)*np.cos(c)],
                            [-np.sin(b), np.sin(a)*np.cos(b), np.cos(a)*np.cos(b)]])
    return np.matmul(rotation_matrix, vector)

def rotateAroundAxis(v, axis, angle):
    #vector: [ux, uy, uz]
    t = np.pi/180 * angle
    rotation_matrix = np.array([[np.cos(t) +pow(axis[2], 2)*(1-np.cos(t)), axis[0]*axis[1]*(1-np.cos(t)) - axis[2]*np.sin(t), axis[0]*axis[2]*(1-np.cos(t)) + axis[1]*np.sin(t)],
                                [axis[1]*axis[0]*(1-np.cos(t)) + axis[2]*np.sin(t), np.cos(t)+pow(axis[1], 2)*(1-np.cos(t)), axis[1]*axis[2]*(1-np.cos(t))-axis[0]*np.sin(t)],
                                [axis[2]*axis[0]*(1-np.cos(t))-axis[1]*np.sin(t), axis[2]*axis[1]*(1-np.cos(t))+axis[0]*np.sin(t), np.cos(t)+pow(axis[2], 2)*(1-np.cos(t))]])
    return np.matmul(rotation_matrix, v)


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


angle_a = 0
angle_b = 0
angle_c = 0

last_tracking_update = 0
rot_axis = np.array([0,0,0])  

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
        angle_a = angle_a - 0.2
    if a[0] > 320 or a[0] < 40 and a[1] > 0.5:
        angle_a = angle_a + 0.2

    if button_turn_right.getValue():
        angle_b = angle_b - 0.2
    if button_turn_left.getValue():
        angle_b = angle_b + 0.2

    if button_set_axis.getValue():
        rot_axis = rotateNormal(np.array([1,0,0]), angle_a, angle_b, angle_c)


    if button_track.getValue():
        if last_tracking_update == 0:
            pass
        else:
            #new_pos = rotateAroundAxis(np.array([angle_a, angle_b, angle_c]), rot_axis, -((time.time() - last_tracking_update)/86164 * 360))
            new_pos = rotateAroundAxis(np.array([angle_a, angle_b, angle_c]), rot_axis, -((time.time() - last_tracking_update)/60 * 360))
            angle_a = new_pos[0]
            angle_b = new_pos[1]
            angle_c = new_pos[2]
        last_tracking_update = time.time()


    
    line = 'A' + str(round(angle_a, 2)) + ' B' + str(round(angle_b, 2)) +' C' + str(round(angle_c, 2)) + '\n'
    tracker.write(line.encode('UTF-8'))
    print(line)
    time.sleep(0.02)
    pygame.display.flip()