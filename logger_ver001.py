#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 23:19:51 2017

@author: Nikolaus Rieder
Logging Module for Alarm System - ver001
"""

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

