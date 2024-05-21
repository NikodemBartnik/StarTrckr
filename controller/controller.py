import pygame, time, gui
import serial
import TrackerController
import PlotVisualizer

pygame.init()
screen = pygame.display.set_mode([800, 600])

SERIALPORT ='/dev/cu.usbmodem14201'
tracker = serial.Serial(SERIALPORT, 115200, timeout=0.01)

mousePressed = False
tc = TrackerController.TrackerController()
plotVisualizer = None
setAxis = False



def clickCheck(pos, clicked):
    joystick.checkIfPressed(pos, clicked)
    button_turn_left.checkIfPressed(pos, clicked)
    button_turn_right.checkIfPressed(pos, clicked)
    button_set_axis.checkIfPressed(pos, clicked)
    button_track.checkIfPressed(pos, clicked)
    slider_movement_precision.checkIfPressed(pos, clicked)

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
    slider_movement_precision.draw(screen)
    title_a_pos.draw(screen)
    title_b_pos.draw(screen)
    title_c_pos.draw(screen)


def WaitForOK():
    while(1):
        if(tracker.readline() == b'OK\n'):
            break


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
slider_movement_precision = gui.Slider((100, 380), 300, 0.5, 0, 1)
title_a_pos = gui.Title((580, 420), '0')
title_b_pos = gui.Title((580, 450), '0')
title_c_pos = gui.Title((580, 480), '0')


last_tracking_update = 0


while 1:
    keyPressed = pygame.key.get_pressed()
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
    movementPrecision = slider_movement_precision.getValue()
    if (a[0] > 50 and a[0] < 130 and a[1] > 0.5) or keyPressed[pygame.K_UP]:
        tc.rotateAltitude(-movementPrecision)
    if (a[0] > 230 and a[0] < 310 and a[1] > 0.5) or keyPressed[pygame.K_DOWN]:
        tc.rotateAltitude(movementPrecision)

    if (a[0] > 140 and a[0] < 210 and a[1] > 0.5) or keyPressed[pygame.K_RIGHT]:
        tc.rotateAzimuth(movementPrecision)
    if (a[0] > 320 or a[0] < 40 and a[1] > 0.5) or keyPressed[pygame.K_LEFT]:
       tc.rotateAzimuth(-movementPrecision)

    if button_turn_right.getValue():
        tc.rotateField(-movementPrecision)
    if button_turn_left.getValue():
        tc.rotateField(movementPrecision)

    if button_set_axis.getValue():
        tc.polarAlign()
        #plotVisualizer = PlotVisualizer.PlotVisualizer(tc.getRefVecX(), tc.getRefVecZ(), tc.getPolarVecX(), tc.getPolarVecZ(), tc.getTrackerVecX(), tc.getTrackerVecZ())
        setAxis = True
        title_angle.change('Axis ready!')

    if button_track.getValue():
        if last_tracking_update == 0:
            pass
        else:
            #86164
            tc.track(((time.time() - last_tracking_update)/86164 * 360))
        last_tracking_update = time.time()

    
    #if(setAxis):
        #plotVisualizer.updateVectors(tc.getRefVecX(), tc.getRefVecZ(), tc.getPolarVecX(), tc.getPolarVecZ(), tc.getTrackerVecX(), tc.getTrackerVecZ(), tc.getC(), tc.getB(), tc.getA())
        
    print("RA: " + str(tc.getRA()) + " DEC: " + str(tc.getDEC()) + " C: " + str(tc.getC()))
    try:
        title_a_pos.change('RA: ' + tc.getRA())
        title_b_pos.change('DEC: ' + tc.getDEC())
        title_c_pos.change('C: ' + tc.getC())
    except:
        print('Nan exception')
    line = 'A' + str(tc.getA()) + ' B' + str(tc.getB()) +' C' + str(tc.getC()) + '\n'
    tracker.write(line.encode('UTF-8'))
    #print(line)
    time.sleep(0.02)
    pygame.display.flip()