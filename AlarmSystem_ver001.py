#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 03:29:46 2017

@author: Nikolaus Rieder
"""

#Libraries Imports
import picamera
import RPi.GPIO as GPIO
import time

def pir_callback(channel):
    print ("Movement. Activating Camera!")
    camera.start_preview()
    time.sleep(2)
    camera.stop_preview()
def reed_callback(channel):
    print ("DOOR OPENED!")
def vib_callback(channel):
    print ("WINDOW SMASHED!")

GPIO.setmode(GPIO.BOARD)

#PreDefined Shortcuts
IN = GPIO.IN
OUT = GPIO.OUT
input = GPIO.input
output = GPIO.output
camera = picamera.PiCamera()

#REED
GPIO.setup(37, IN, pull_up_down=GPIO.PUD_DOWN)
#PIR
GPIO.setup(36, IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(38, IN, pull_up_down=GPIO.PUD_DOWN)
#ServoMotor - Pan(35) / Tilt(33) - Tilt derzeit nicht notwendig
#GPIO.setup(33, OUT)
GPIO.setup(35, OUT)
GPIO.add_event_detect(36, GPIO.RISING, callback=pir_callback, bouncetime=200)
GPIO.add_event_detect(37, GPIO.RISING, callback=reed_callback, bouncetime=500)
GPIO.add_event_detect(38, GPIO.RISING, callback=vib_callback, bouncetime=1000)

#Pin 35 mit PWM-Frequenz von 50Hz belegen
pan = GPIO.PWM(35, 50)
#tilt = GPIO.PWM(33,50)

#Servo initialisieren
pan.start(2.5)
#tilt = 

try:
    #temp = 0.5
    while True:
        """
        for i in range(24):
            pan.ChangeDutyCycle(temp)
            #print (temp)
            time.sleep(0.2)
            temp += 0.5
        if (temp==12.5):
            for i in range(24):
                pan.ChangeDutyCycle(temp)
                #print (temp)
                time.sleep(0.2)
                temp -= 0.5
            if (temp==2.5):
                print ("Restarting...")
                pan.ChangeDutyCycle(0)
                time.sleep(3)
            else:
                print ("Error")
        else:
            print ("Error")
        """
except KeyboardInterrupt:
    pan.stop()
    #tilt.stop()
    GPIO.cleanup()