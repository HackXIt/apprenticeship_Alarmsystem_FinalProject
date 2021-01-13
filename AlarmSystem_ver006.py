
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 22:02:35 2017

@author: Nikolaus Rieder
Changes in ver006
Camera Implementation (USB Cameras)
Modulized logging and Alarmviewer (less imports here)
"""

#Library Imports
import RPi.GPIO as GPIO
import time
import logging
import weakref
import AlarmViewer_ver002 as av
#import tkinter as tk
#import threading as th
#import logger_ver001

GPIO.setmode(GPIO.BOARD)
#time_stamp = time.time()

class Alarm:
    __status = None
    _components = set()
    states = {}
    components = {}
    runtime = False
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
            self.addEvent('Up', 350, cb_param)
        self._components.add(weakref.ref(self))
        self.createEntry()
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
    def setMode():
        Alarm.__status = av.Alarmviewer.getMode()
    def activate(self):
        if Alarm.status() != 'Disarmed':
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
    def createEntry(self):
        if (self.name != 'Switch') and (self.IO != 'output'):
            Alarm.components[self.pin] = self.name
            Alarm.states[self.name] = None
    def changeState(pin):
        try:
            now = time.localtime(time.time())
            Alarm.states[Alarm.components.get(pin)] = time.strftime("%Y|%m|%d %H:%M:%S", now)
            av.Alarmviewer.updateList(Alarm.states)
        except KeyError:
            logging.error('Component not found')
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
    @classmethod
    def cleaner(cls):
        for obj in cls.listComponents():
            if hasattr(obj, 'callback_func'):
                GPIO.remove_event_detect(obj.pin)
                logging.info('Terminated %s', obj.name)
        GPIO.cleanup()
        logging.info('Cleaned GPIO')
    
def PIRcallback(channel):
    #print ('Alarm detected: ' + PIR.name + '\nMotion Alert!')
    logging.warning('MOTION Alarm detected by %s', channel)
    Alarm.changeState(channel)
def REEDcallback(channel):
    #print ('Alarm detected: ' + REED.name + '\nDoor opened!')
    logging.warning('REED Alarm detected by %s', channel)
    Alarm.changeState(channel)
def VIBRcallback(channel):
    #print ('Alarm detected: ' + VIBR.name + '\nWindow smashed!')
    logging.warning('VIBRATION Alarm detected by %s', channel)
    Alarm.changeState(channel)
def ModeSet(channel):
    Alarm.setMode()
    #print(Alarm.status())
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
#    logging.info('No Mode Switch Configured')
                   
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
switch = Alarm('input', 35, 'Switch', ModeSet)
switch.activate()

#Testing Class Init     
REED = Alarm('input', 37, 'REED', REEDcallback)
PIR = Alarm('input', 36, 'PIR', PIRcallback)
VIBR = Alarm('input', 38, 'VIBR', VIBRcallback)
LED = Alarm('output', 40, 'LED')

#DUMMY Dictionary for Debugging
statusD = {'Example':'2017|11|14 15:32:13', 
               'PIR':'2017|10|14 13:15:54',
               'VIBR':'2017|09|16 08:45:10'}
global finish
finish = False
global updateAttempts
updateAttempts = 0
def update():
    global updateAttempts
    try:
        GUI.updateList(Alarm.states)
        logging.info('Time Stamp. Updated.')
    except AttributeError:
        updateAttempts += 1
        if updateAttempts <= 3:
            logging.debug('Main window not initialized')
    finally:
        if GUI.parent.state() == 'normal':
            GUI.parent.after(10000, update)
        elif GUI.parent.state() == 'withdrawn':
            if updateAttempts <= 3: 
                GUI.parent.after(5000, update)
            else:
                logging.error('Aborting.')
                GUI.pop.destroy()
                GUI.parent.quit()


#root = tk.Tk()
#GUI = av.Alarmviewer(root)
#GUI.after(10000, update)
#GUI.mainloop()
GUI = av.start()
GUI.after(10000, update)
GUI.mainloop()
#After Window Closed
finish = True
logging.info('Terminating Components...')
Alarm.cleaner()