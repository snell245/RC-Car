from pynput.keyboard import Key, Listener
import l293d.driver as l293d
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
# Drive Motor
MotorA1 = 13
MotorA2 = 11
MotorA3 = 15

# Steering Motor
MotorB1 = 16
MotorB2 = 18
MotorB3 = 22

GPIO.setup(MotorA1, GPIO.OUT)
GPIO.setup(MotorA2, GPIO.OUT)
GPIO.setup(MotorA3, GPIO.OUT)

GPIO.setup(MotorB1, GPIO.OUT)
GPIO.setup(MotorB2, GPIO.OUT)
GPIO.setup(MotorB3, GPIO.OUT)

# p = GPIO.PWM(MotorA2, 0.5)
# p.start(50)

keepGoing = True

while keepGoing:

    def press_down(key):
        if key == Key.up:
            GPIO.output(MotorA1, GPIO.LOW)
            GPIO.output(MotorA2, GPIO.HIGH)
            GPIO.output(MotorA3, GPIO.HIGH)
        if key == Key.down:
            GPIO.output(MotorA1, GPIO.HIGH)
            GPIO.output(MotorA2, GPIO.LOW)
            GPIO.output(MotorA3, GPIO.HIGH)
        if key == key.left:
            GPIO.output(MotorB1, GPIO.HIGH)
            GPIO.output(MotorB2, GPIO.LOW)
            GPIO.output(MotorB3, GPIO.HIGH)
            # p.ChangeDutyCycle(100)
        if key == key.right:
            GPIO.output(MotorB1, GPIO.LOW)
            GPIO.output(MotorB2, GPIO.HIGH)
            GPIO.output(MotorB3, GPIO.HIGH)
            # p.ChangeDutyCycle(50)


    def release(key):
        if key == Key.up:
            GPIO.output(MotorA3, GPIO.LOW)
        if key == Key.down:
            GPIO.output(MotorA3, GPIO.LOW)
        if key == Key.left:
            GPIO.output(MotorB3, GPIO.LOW)
        if key == key.right:
            GPIO.output(MotorB3, GPIO.LOW)

        if key == Key.esc:
            keepGoing = False
            l293d.cleanup()
            GPIO.cleanup()
            return False


    with Listener(
            on_press=press_down,
            on_release=release) as listener:
        listener.join()
