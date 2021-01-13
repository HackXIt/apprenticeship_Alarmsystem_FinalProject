#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 15:24:54 2017

@author: Nikolaus Rieder
Changes in ver003
Logging - Done
AlarmStatus (Armed, Disarmed) - Done
"""

#Library Imports
import RPi.GPIO as GPIO
import time
import logging

GPIO.setmode(GPIO.BOARD)
#time_stamp = time.time()

#DISPLAY TEXTS
global modeError 
modeError = 'Incorrect mode given'
global declarationError
declarationError = 'No input/output declared'
global codeWarning
codeWarning = 'Incorrect code! Retry please...'
global attemptWarning
attemptWarning = 'Maximum Attempts reached! Calling security...'

class Alarm:
    __status = None
    __code = None
    def __init__(self, IO, pin, Name, cb_param):
        self.IO = IO
        self.pin = pin
        self.Name = Name
        self.callback_func = cb_param
        if IO == 'input':
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        elif IO == 'output':
            GPIO.setup(pin, GPIO.OUT)
        else:
            logging.error(declarationError)
        self.addEvent('Up', 250)
    def addEvent(self, UpDown, btime):
        if UpDown == 'Up':
            UpDown = GPIO.RISING
        elif UpDown == 'Down':
            UpDown = GPIO.FALLING
        logging.info('Adding %s', self.Name)
        GPIO.add_event_detect(self.pin, UpDown, self.callback_func, btime)
    def getPin(self):
        return self.pin
    def cleaning(self):
        GPIO.remove_event_detect(self.pin)
    def Status():
        return Alarm.__status
    def SetCode(code):
        Alarm.__code = code
    def setAlarmState(mode):
        attempts = 0
        if mode == 'Arm':
            while attempts < 3:
                if input('Input code: ') == Alarm.__code:
                    Alarm.__status = 'Armed'
                    break
                else:
                    logging.warning(codeWarning)
                    attempts += 1
            else:
                logging.critical(attemptWarning)
        elif mode == 'Disarm':
            while attempts < 3:
                if input('Input code: ') == Alarm.__code:
                    Alarm.__status = 'Disarmed'
                    break
                else:
                    logging.warning(codeWarning)
                    attempts += 1
            else:
                logging.critical(attemptWarning)
        else:
            logging.error(modeError)
            
    
def PIRcallback(channel):
    #print ('Alarm detected: ' + PIR.Name + '\nMotion Alert!')
    logging.warning('MOTION Alarm detected by %s', channel)
def REEDcallback(channel):
    #print ('Alarm detected: ' + REED.Name + '\nDoor opened!')
    logging.warning('REED Alarm detected by %s', channel)
def VIBRcallback(channel):
    #print ('Alarm detected: ' + VIBR.Name + '\nWindow smashed!')
    logging.warning('VIBRATION Alarm detected by %s', channel)
def ModeSet(channel):
    Alarm.setAlarmState(input('Set Alarm Mode to: '))
    logging.info(Alarm.Status())
    
#Logging Setup, needs to be modulized
FORMAT = '%(asctime)s, %(levelname)s: %(message)s'
DATEFMT = '%d|%m|%y, %H:%M:%S'
logger = logging.getLogger()
fhandler = logging.FileHandler(filename='logger.log', mode='w')
formatter = logging.Formatter(FORMAT)
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)
logger.setLevel(logging.DEBUG)

#Testing Code/Status Setup
Alarm.SetCode(input('Set the code to: '))
switch = Alarm('input', 10, 'Switch', ModeSet)

#Testing Class Init     
REED = Alarm('input', 37, "REED", REEDcallback)
PIR = Alarm('input', 36, "PIR", PIRcallback)
VIBR = Alarm('input', 38, "VIBR", VIBRcallback)

try:
    while True:
        #'REED'
        #print (GPIO.input(37))
        #'PIR'
        #print (GPIO.input(36))
        #'VIBR'
        #print (GPIO.input(38))
        time.sleep(60)
        logging.info('Time Stamp')
        
        #MAIN PROGRAM - Currently does nothing, 
        #triggers work via parallel threading
        
except KeyboardInterrupt:
    logging.warning('Terminating program...')
    time.sleep(1)
finally:
    REED.cleaning()
    PIR.cleaning()
    VIBR.cleaning()
    switch.cleaning()
    GPIO.cleanup()
    logging.info('Cleaned GPIO!')