from pynput.keyboard import Key, Listener
import l293d.driver as l293d
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

Motor1 = 13
Motor2 = 11
Motor3 = 15

GPIO.setup(Motor1, GPIO.OUT)
GPIO.setup(Motor2, GPIO.OUT)
GPIO.setup(Motor3, GPIO.OUT)

keepGoing = True

while keepGoing:

    def press_down(key):
        if key == Key.up:
            GPIO.output(Motor1, GPIO.LOW)
            GPIO.output(Motor2, GPIO.HIGH)
            GPIO.output(Motor3, GPIO.HIGH)
        if key == Key.down:
            GPIO.output(Motor1, GPIO.HIGH)
            GPIO.output(Motor2, GPIO.LOW)
            GPIO.output(Motor3, GPIO.HIGH)
        # if key == key.left:

        # if key == key.right:


    def release(key):
        if key == Key.up:
            GPIO.output(Motor3, GPIO.LOW)
        if key == Key.down:
            GPIO.output(Motor3, GPIO.LOW)
        # if key == Key.left:
        # if key == key.right:
        if key == Key.esc:
            keepGoing = False
            l293d.cleanup()
            GPIO.cleanup()
            return False


    with Listener(
            on_press=press_down,
            on_release=release) as listener:
        listener.join()