#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 14:31:50 2017

@author: Nikolaus Rieder
Testing Environment
"""

#Test USB-Camera (SingleImageCapture)
#import pygame
#import pygame.camera
##from pygame.locals import *
#
#pygame.init()
#pygame.camera.init()
#
#DEVICE = '/dev/video0'
#SIZE = (640, 480)
#FILENAME = 'capture.png'
#
#camera = pygame.camera.Camera(DEVICE, SIZE)
#camera.start()
##size = camera.get_size()
##print(size)
##camera.set_controls()
#img = camera.get_image()
#pygame.image.save(img, FILENAME)
#camera.stop()


#Test Event Detection
#import RPi.GPIO as GPIO
#
#PIN = 36
#IO = GPIO.IN
#EDGE = GPIO.RISING
#
#def detected(channel):
#    print ('Interrupt EDGE detected')
#
#GPIO.setmode(GPIO.BOARD)
##GPIO.setup(PIN, IO, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(36, GPIO.IN)
#GPIO.add_event_detect(PIN, EDGE, detected, 350)
#
#
#try:
#    while True:
#        pass
#except KeyboardInterrupt:
#    print ('Done')
#finally:
#    GPIO.remove_event_detect(PIN)
#    GPIO.cleanup()
        