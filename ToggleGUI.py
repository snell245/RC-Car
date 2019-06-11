from __future__ import division
from pynput.keyboard import Key, Listener
#import l293d.driver as l293d
import RPi.GPIO as GPIO
from gpiozero import DistanceSensor
import time
import random
import wx
import wx.lib.buttons as buttons

GPIO.setmode(GPIO.BCM)

# Drive Motor
MotorA1 = 27
MotorA2 = 17
MotorA3 = 22

# Steering Motor
MotorB1 = 23
MotorB2 = 24
MotorB3 = 25


GPIO.setup(MotorA1,GPIO.OUT)
GPIO.setup(MotorA2,GPIO.OUT)
GPIO.setup(MotorA3,GPIO.OUT)

GPIO.setup(MotorB1,GPIO.OUT)
GPIO.setup(MotorB2,GPIO.OUT)
GPIO.setup(MotorB3,GPIO.OUT)

ultrasonic = DistanceSensor(echo=20, trigger=21)

#p = GPIO.PWM(MotorA2, 0.5)
#p.start(50)

keepGoing = True



class MyForm(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "RC Extreme!")
        panel = wx.Panel(self, wx.ID_ANY)

        
        button = wx.ToggleButton(panel, label="Autopilot")
        button.Bind(wx.EVT_TOGGLEBUTTON, self.onToggle)

        gen_toggle_button = buttons.GenToggleButton(panel, -1, "User Control")
        gen_toggle_button.Bind(wx.EVT_BUTTON, self.onGenericToggle)


        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(button, 0, wx.ALL, 5)
        sizer.Add(gen_toggle_button, 0, wx.ALL, 5)
        panel.SetSizer(sizer)

    def onGenericToggle(self, eventq):
        
        while keepGoing:

            def press_down(key):
                if key == Key.up:
                    GPIO.output(MotorA1,GPIO.LOW)
                    GPIO.output(MotorA2,GPIO.HIGH)
                    GPIO.output(MotorA3,GPIO.HIGH)
                if key == Key.down:
                    GPIO.output(MotorA1,GPIO.HIGH)
                    GPIO.output(MotorA2,GPIO.LOW)
                    GPIO.output(MotorA3,GPIO.HIGH)
                if key == key.left:
                    GPIO.output(MotorB1,GPIO.HIGH)
                    GPIO.output(MotorB2,GPIO.LOW)
                    GPIO.output(MotorB3,GPIO.HIGH)
                    #p.ChangeDutyCycle(100)
                if key == key.right:
                    GPIO.output(MotorB1,GPIO.LOW)
                    GPIO.output(MotorB2,GPIO.HIGH)
                    GPIO.output(MotorB3,GPIO.HIGH)
                    #p.ChangeDutyCycle(50)

            def release(key):
                if key == Key.up:
                    GPIO.output(MotorA3,GPIO.LOW)
                if key == Key.down:
                    GPIO.output(MotorA3,GPIO.LOW)
                if key == Key.left:
                    GPIO.output(MotorB3,GPIO.LOW)
                if key == key.right:
                    GPIO.output(MotorB3,GPIO.LOW)
            
                if key == Key.esc:
                    keepGoing = False
                    #l293d.cleanup()
                    GPIO.cleanup()
                    #return False
    
            with Listener(
                on_press=press_down,
                on_release=release) as listener:
                listener.join()



    def onToggle(self, event):
        
        randy = random.randint(1,2)
        try:
    
            while keepGoing:
                #print("During Loop")
        
                #randy = random.randint(1,2)
                #print randy
                def TooCloseForComfort():
                    #randy = random.randint(1,2)
            
                    #Forward
                    if (ultrasonic.distance / 0.01) > 50:
                        time.sleep(2)
                        GPIO.output(MotorA1, GPIO.LOW)
                        GPIO.output(MotorA2, GPIO.HIGH)
                        GPIO.output(MotorA3, GPIO.HIGH)
                        if (ultrasonic.distance / 0.01) < 50:
                            GPIO.output(MotorA3, GPIO.LOW)
                            time.sleep(4)
                
                    #time.sleep(4)
            
                    #Reverse
                    if (ultrasonic.distance / 0.01) < 50:
                        time.sleep(2)
                        GPIO.output(MotorA1, GPIO.HIGH)
                        GPIO.output(MotorA2, GPIO.LOW)
                        GPIO.output(MotorA3, GPIO.HIGH)
                        if (ultrasonic.distance / 0.01) > 50:
                            GPIO.output(MotorA3, GPIO.LOW)
                            time.sleep(4)
                    #Left
                    if (ultrasonic.distance / 0.01) < 50 and randy == 1:
                        GPIO.output(MotorB1, GPIO.HIGH)
                        GPIO.output(MotorB2, GPIO.LOW)
                        GPIO.output(MotorB3, GPIO.HIGH)
                    #Right
                    if (ultrasonic.distance / 0.01) < 50 and randy == 2:
                        GPIO.output(MotorB1, GPIO.LOW)
                        GPIO.output(MotorB2, GPIO.HIGH)
                        GPIO.output(MotorB3, GPIO.HIGH)


                def StopMotor():
                    if (ultrasonic.distance / 0.01) > 50:
                        GPIO.output(MotorB3, GPIO.LOW)
            
                TooCloseForComfort()
                StopMotor()

        except KeyboardInterrupt:
            GPIO.cleanup()
            print("Stop!")


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()
