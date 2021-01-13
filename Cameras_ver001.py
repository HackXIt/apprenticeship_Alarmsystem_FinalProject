#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 22:10:56 2017

@author: pi
"""
#from picamera import PiCamera
#import pygame
#import pygame.camera
#from pygame.locals import *
##import threading as th
#import tkinter as tk

import cv2
#import time
#
#cv.NamedWindow('w1', cv.CV_WINDOW_AUTOSIZE)
#capture = cv.CaptureFromCAM(0)
#
#def repeat():
#    
#    frame = cv.QueryFrame(capture)
#    cv.ShowImage('w1', frame)
#    
#while True:
#    repeat()
#    time.sleep(2)

#class livefeed(pygame.camera.init):
#    def __init__(self, window):
#        self.size = (640, 480)
#        self.display = window
#        self.clist = pygame.camera.list_cameras()
#        if not self.clist:
#            raise ValueError('No cameras detected.')
#        self.cam = pygame.camera.Camera(self.clist[0], self.size)
#        self.cam.start()
#        
#    def capture(self):
#        print (self.cam.query_image()) # DEBUG
#        if self.cam.query_image():
#            self.
#
#pygame.camera.list_cameras()
#
#class USBcamera(object):
#    
#class piCam():
    