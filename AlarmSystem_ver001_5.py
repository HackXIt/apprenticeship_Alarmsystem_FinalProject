#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 13:04:07 2017

@author: Nikolaus Rieder
"""

#Library Imports
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
time_stamp = time.time()

class AlarmSetup:
    __passkey = "P@ssw0rd"
    __status = None
    def __init__(self, IO, pin, Name):
        self.IO = IO
        self.pin = pin
        self.Name = Name
        if (IO == 'input'):
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        elif (IO == 'output'):
            GPIO.setup(pin, GPIO.OUT)
        else:
            print ('Error: No input/output declared')
    def addEvent(self, UpDown, callback, btime):
        if (UpDown == 'Up'):
            UpDown = GPIO.RISING
        elif (UpDown == 'Down'):
            UpDown = GPIO.FALLING
        GPIO.add_event_detect(self.pin, UpDown, callback=callback, bouncetime=btime)
    def getPin(self):
        return self.pin
    def Status(self, password, status):
        if (password == AlarmSetup.__passkey):
            AlarmSetup.__status = status
        else:
            print ('Wrong Password')

def PIRcallback(channel):
    global time_stamp
    time_now = time.time()
    if (time_now - time_stamp) >= 0.3:
        print ("Motion Alarm on " + str(channel))
    time_stamp = time_now
def REEDcallback(channel):
    global time_stamp
    time_now = time.time()
    if (time_now - time_stamp) >= 0.3:
        print ("Door Alarm on " + str(channel))
    time_stamp = time_now
def VIBRcallback(channel):
    global time_stamp
    time_now = time.time()
    if (time_now - time_stamp) >= 0.3:
        print ("Window Alarm on " + str(channel))
    time_stamp = time_now
    
        
#Testing Class Init
REED = AlarmSetup('input', 37, "Reed")
PIR = AlarmSetup('input', 36, "PIR")
VIBR = AlarmSetup('input', 38, "Vibrationssensor")
VIBR.addEvent('Up', VIBRcallback, 500)
PIR.addEvent('Up', PIRcallback, 500)
REED.addEvent('Up', REEDcallback, 500)

try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
    print ("Cleaned")