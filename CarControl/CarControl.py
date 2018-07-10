from pynput.keyboard import Key, Listener
import l293d.driver as l293d
import RPi.GPIO as GPIO

# l293d.cleanup()
# GPIO.cleanup()

# Motor 1 uses Pin 22, Pin 18, Pin 16
motor1 = l293d.DC(22, 18, 16)
# Motor 2 uses Pin 15, Pin 13, Pin 11
motor2 = l293d.DC(15, 13, 11)

# Run the motors so visible
# for i in range(0,500):
# motor1.clockwise()
# motor2.clockwise()

# motor1.stop()
# motor2.stop()
# l293d.cleanup()
# GPIO.cleanup()

# Line Drawn Here
upButton = True
downButton = True
leftButton = True
rightButton = True
keepGoing = True

while keepGoing:

    def press_down(key):
        if key == Key.up:
            while upButton:
                motor2.anticlockwise()
        if key == Key.down:
            while downButton:
                motor2.clockwise()
        if key == key.left:
            while leftButton:
                motor1.anticlockwise()
        if key == key.right:
            while rightButton:
                motor1.clockwise()


    def release(key):
        if key == Key.up:
            upButton = False
            # motor1.stop()
        if key == Key.down:
            downButton = False
            # motor1.stop()
        if key == Key.left:
            leftButton = False
            # motor2.stop()
        if key == key.right:
            rightButton = False
            # motor2.stop()

        if key == Key.esc:
            keepGoing = False
            l293d.cleanup()
            GPIO.cleanup()
            return False

with Listener(
        on_press=press_down,
        on_release=release) as listener:
    listener.join()

# import l293d

# motor1 = l293d.DC(15,13,11)

# motor1.clockwise()

# l293d.cleanup()

# from gpiozero import Motor
# from time import sleep

# motor1 = Motor(22,18,16)
# motor2 = Motor(15,13,11)

# motor1.forward()
# sleep(2)
# motor1.backward()
# sleep(2)
# motor1.stop()

# motor2.forward()
# sleep(2)
# motor2.backward()
# sleep(2)
# motor2.stop()
