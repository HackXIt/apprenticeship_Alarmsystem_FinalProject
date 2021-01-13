#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 12:57:20 2017

@author: Nikolaus Rieder
Modularisierung des bestehenden Systems
"""

#Library Imports
import RPi.GPIO as GPIO
import time
import logging
import weakref
#import tkinter as tk
#import AlarmViewer

GPIO.setmode(GPIO.BOARD)
#time_stamp = time.time()

#DISPLAY TEXTS
global modeError, declarationError, codeWarning, attemptWarning, statusError, edgeConflict, runtimeError1, runtimeError2
modeError = 'Incorrect mode given'
declarationError = 'No input/output declared'
codeWarning = 'Incorrect code! Retry please...'
attemptWarning = 'Maximum Attempts reached! Calling security...'
statusError = 'Alarm System not armed.'
edgeConflict = 'Conflicting edge detection already enabled for this GPIO channel'
runtimeError1 = 'Alarm already disarmed. Please arm the system.'
runtimeError2 = 'Alarm already armed. Please disarm the sytem if necessary.'

class Alarm:
    __status = None
    __code = None
    _components = set()
    states = [[],[]]
    runtime = False
    #__wrongCode = set()
    #Logging of unsuccessful logins with timestamps. ToDo
    def __init__(self, IO, pin, name, cb_param=None):
        self.IO = IO
        self.pin = pin
        self.name = name
        if IO == 'input':
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        elif IO == 'output':
            GPIO.setup(pin, GPIO.OUT)
        else:
            logging.error(declarationError)
        if cb_param is not None:
            self.addEvent('Up', 250, cb_param)
        self._components.add(weakref.ref(self))
    def addEvent(self, edge, btime, cb_param):
        self.btime = btime
        if edge == 'Up':
            self.edge = GPIO.RISING
        elif edge == 'Down':
            self.edge = GPIO.FALLING
        self.callback_func = cb_param
        logging.info('Added %s', self.name)
    def getPin(self):
        return self.pin
    def deactivate(self):
        if (Alarm.status() is not 'Armed') and (self.name is not 'Switch'):
            if hasattr(self, 'callback_func'):
                GPIO.remove_event_detect(self.pin)
                logging.info('Deactivated %s', self.name)
    def status():
        return Alarm.__status
    def setCode(code):
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
                #Alarm.__wrongCode.add(1, )
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
    def activate(self):
        if Alarm.status() is not 'Disarmed':
            try:
                GPIO.add_event_detect(self.pin, self.edge, 
                                      self.callback_func, self.btime)
                logging.info('Activated %s', self.name)
            except RuntimeError: # Can't overwrite existing detection
                if self.name is not 'Switch':
                    logging.error(edgeConflict)
            except AttributeError: # No callback function provided
                if self.IO == 'output':
                    GPIO.output(self.pin, GPIO.HIGH)
    @classmethod
    def listComponents(cls):
        dead = set()
        for ref in cls._components:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._components -= dead
    @staticmethod
    def Cleaner():
        for obj in Alarm.listComponents():
            if hasattr(obj, 'callback_func'):
                GPIO.remove_event_detect(obj.pin)
                logging.info('Terminated %s', obj.name)
        GPIO.cleanup()
        logging.info('Cleaned GPIO')
    
def PIRcallback(channel):
    #print ('Alarm detected: ' + PIR.name + '\nMotion Alert!')
    logging.warning('MOTION Alarm detected by %s', channel)
def REEDcallback(channel):
    #print ('Alarm detected: ' + REED.name + '\nDoor opened!')
    logging.warning('REED Alarm detected by %s', channel)
def VIBRcallback(channel):
    #print ('Alarm detected: ' + VIBR.name + '\nWindow smashed!')
    logging.warning('VIBRATION Alarm detected by %s', channel)
def ModeSet(channel):
    Alarm.setAlarmState(input('Set Alarm Mode to (Arm, Disarm): '))
    if (Alarm.status() is 'Armed') and (Alarm.runtime == False):
        for obj in Alarm.listComponents():
            obj.activate()
        Alarm.runtime = True
        logging.info(Alarm.status())
    elif (Alarm.status() is 'Disarmed') and (Alarm.runtime == True):
        for obj in Alarm.listComponents():
            obj.deactivate()
        Alarm.runtime = False
        logging.info(Alarm.status())
    else:
        if Alarm.runtime:
            logging.error(runtimeError2)
        elif not Alarm.runtime:
            logging.error(runtimeError1)

                        
#Logging Setup, needs to be modulized
FORMAT = '%(asctime)s, %(levelname)s: %(message)s'
DATEFMT = '%d|%m|%y, %H:%M:%S'
logger = logging.getLogger()
fhandler = logging.FileHandler(filename='logger.log', mode='w')
formatter = logging.Formatter(FORMAT, DATEFMT)
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)
logger.setLevel(logging.DEBUG)
logger.propagate = True

#Testing Code/status Setup
Alarm.setCode(input('Set the code to: '))
switch = Alarm('input', 35, 'Switch', ModeSet)
switch.activate()

#Testing Class Init     
REED = Alarm('input', 37, 'REED', REEDcallback)
PIR = Alarm('input', 36, 'PIR', PIRcallback)
VIBR = Alarm('input', 38, 'VIBR', VIBRcallback)
LED = Alarm('output', 40, 'LED')

#Testing Alarmviewer Init
#root = tk.Tk()
#viewer = AlarmViewer(root)
#root.mainloop()

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
    Alarm.Cleaner()