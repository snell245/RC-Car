# Libraries
from pynput.keyboard import Key, Listener
import l293d.driver as l293d
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 21
GPIO_ECHO = 20

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print(dist)
            #print("Measured Distance = %.1f cm" % dist)
            time.sleep(1)

        # Reset by pressing CTRL + C
    # except KeyboardInterrupt:
    #     print("Measurement stopped by User")
    #     GPIO.cleanup()

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

    dist = distance()
    print(dist)
    # print("Measured Distance = %.1f cm" % dist)
    time.sleep(1)

    def TooCloseForComfort(dist):
        #Forward
        if dist > 20:
            GPIO.output(MotorA1, GPIO.LOW)
            GPIO.output(MotorA2, GPIO.HIGH)
            GPIO.output(MotorA3, GPIO.HIGH)
        #Reverse
        if dist < 20:
            GPIO.output(MotorA1, GPIO.HIGH)
            GPIO.output(MotorA2, GPIO.LOW)
            GPIO.output(MotorA3, GPIO.HIGH)
        #Left
        if dist < 20:
            GPIO.output(MotorB1, GPIO.HIGH)
            GPIO.output(MotorB2, GPIO.LOW)
            GPIO.output(MotorB3, GPIO.HIGH)
            # p.ChangeDutyCycle(100)
        #Right
        if dist > 20:
            GPIO.output(MotorB1, GPIO.LOW)
            GPIO.output(MotorB2, GPIO.HIGH)
            GPIO.output(MotorB3, GPIO.HIGH)
            # p.ChangeDutyCycle(50)


    def StopMotor(dist):
        #Disable Forward
        if dist < 20:
            GPIO.output(MotorA3, GPIO.LOW)
        #Disable Reverse
        if dist > 20:
            GPIO.output(MotorA3, GPIO.LOW)
        #Disable Left
        if dist > 20:
            GPIO.output(MotorB3, GPIO.LOW)
        #Disable Right
        if dist > 50:
            GPIO.output(MotorB3, GPIO.LOW)

    def StopProgram(key):
        if key == Key.esc:
            keepGoing = False
            l293d.cleanup()
            GPIO.cleanup()
            return False


    with Listener(
            on_press=press_down,
            on_release=release) as listener:
        listener.join()

