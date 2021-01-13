#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 03:29:46 2017

@author: Nikolaus Rieder
"""

#Library Imports
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
time_stamp = time.time()

class Alarm:
    def __init__(self, IO, pin, Name, cb_param):
        self.IO = IO
        self.pin = pin
        self.Name = Name
        self.callback_func = cb_param
        if (IO == 'input'):
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        elif (IO == 'output'):
            GPIO.setup(pin, GPIO.OUT)
        else:
            print ('Error: No input/output declared')
        self.addEvent('Up', 500)
    def addEvent(self, UpDown, btime):
        if (UpDown == 'Up'):
            UpDown = GPIO.RISING
        elif (UpDown == 'Down'):
            UpDown = GPIO.FALLING
        print ('Adding ' + self.Name)
        GPIO.add_event_detect(self.pin, UpDown, self.callback_func, btime)
    def getPin(self):
        return self.pin
    """
    def cb(self):
        global time_stamp
        time_now = time.time()
        time_base = time_now - time_stamp
        print ('TESTING')
        if (time_now - time_stamp) >= 0.4:
            time_stamp = time_now
            print (time_base)
            self.callback_func()
    """
    def cleaning(self):
        GPIO.remove_event_detect(self.pin)
        
def PIRcallback(channel):
    print ('Alarm detected: ' + PIR.Name + '\nMotion Alert!')
def REEDcallback(channel):
    print ('Alarm detected: ' + REED.Name + '\nDoor opened!')
def VIBRcallback(channel):
    print ('Alarm detected: ' + VIBR.Name + '\nWindow smashed!')

#Testing Class Init     
REED = Alarm('input', 37, "REED", REEDcallback)
PIR = Alarm('input', 36, "PIR", PIRcallback)
VIBR = Alarm('input', 38, "VIBR", VIBRcallback)

try:
    while True:
        'REED'
        #print (GPIO.input(37))
        'PIR'
        #print (GPIO.input(36))
        'VIBR'
        #print (GPIO.input(38))
        time.sleep(1)
        
        #MAIN PROGRAM - Currently does nothing, triggers work via parallel threading
        
except KeyboardInterrupt:
    print ("Terminating program...")
    time.sleep(1)
finally:
    REED.cleaning()
    PIR.cleaning()
    VIBR.cleaning()
    GPIO.cleanup()
    print ("Cleaned GPIO!")