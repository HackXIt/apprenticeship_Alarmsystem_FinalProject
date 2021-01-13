#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 15:21:50 2017

@author: Nikolaus Rieder
Logging Module for Package AlarmSystem
"""

import logging

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

#class logs:
#    def __init__: