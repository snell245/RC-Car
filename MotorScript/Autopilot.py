from __future__ import division
from gpiozero import DistanceSensor
from pynput.keyboard import Key, Listener
# import l293d.driver as l293d
import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BCM)

# Drive Motor
MotorA1 = 27
MotorA2 = 17
MotorA3 = 22

# Steering Motor
MotorB1 = 23
MotorB2 = 24
MotorB3 = 25

# GPIO_TRIGGER = 40
# GPIO_ECHO = 38

# GPIO.setmode(GPIO.BOARD)
GPIO.setup(MotorA1, GPIO.OUT)
GPIO.setup(MotorA2, GPIO.OUT)
GPIO.setup(MotorA3, GPIO.OUT)

GPIO.setup(MotorB1, GPIO.OUT)
GPIO.setup(MotorB2, GPIO.OUT)
GPIO.setup(MotorB3, GPIO.OUT)

ultrasonic = DistanceSensor(echo=20, trigger=21)
# p = GPIO.PWM(MotorA2, 0.5)
# p.start(50)
# holdOn = True
keepGoing = True
# print("Before Loop")
randy = random.randint(1, 2)
try:

    while keepGoing:
        # print("During Loop")

        # randy = random.randint(1,2)
        # print randy
        def TooCloseForComfort():
            # randy = random.randint(1,2)

            # Forward
            if (ultrasonic.distance / 0.01) > 50:
                time.sleep(2)
                GPIO.output(MotorA1, GPIO.LOW)
                GPIO.output(MotorA2, GPIO.HIGH)
                GPIO.output(MotorA3, GPIO.HIGH)
                if (ultrasonic.distance / 0.01) < 50:
                    GPIO.output(MotorA3, GPIO.LOW)
                    time.sleep(4)

            # time.sleep(4)

            # Reverse
            if (ultrasonic.distance / 0.01) < 50:
                time.sleep(2)
                GPIO.output(MotorA1, GPIO.HIGH)
                GPIO.output(MotorA2, GPIO.LOW)
                GPIO.output(MotorA3, GPIO.HIGH)
                if (ultrasonic.distance / 0.01) > 50:
                    GPIO.output(MotorA3, GPIO.LOW)
                    time.sleep(4)
            # Left
            if (ultrasonic.distance / 0.01) < 50 and randy == 1:
                GPIO.output(MotorB1, GPIO.HIGH)
                GPIO.output(MotorB2, GPIO.LOW)
                GPIO.output(MotorB3, GPIO.HIGH)
                # p.ChangeDutyCycle(100)
            # Right
            if (ultrasonic.distance / 0.01) < 50 and randy == 2:
                GPIO.output(MotorB1, GPIO.LOW)
                GPIO.output(MotorB2, GPIO.HIGH)
                GPIO.output(MotorB3, GPIO.HIGH)
                # p.ChangeDutyCycle(50)


        def StopMotor():
            # Disable Forward
            # if (ultrasonic.distance / 0.01) < 50:
            # time.sleep(4)
            # GPIO.output(MotorA3, GPIO.LOW)

            # Disable Reverse
            # if (ultrasonic.distance / 0.01) > 50:
            # GPIO.output(MotorA3, GPIO.LOW)
            # Disable Steering
            if (ultrasonic.distance / 0.01) > 50:
                GPIO.output(MotorB3, GPIO.LOW)
            # Disable Right
            # if (ultrasonic.distance / 0.01) > 50:
            # GPIO.output(MotorB3, GPIO.LOW)


        TooCloseForComfort()
        StopMotor()

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Stop!")

