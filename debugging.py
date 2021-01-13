#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 17:40:36 2017

@author: pi
"""
import weakref

class System():
    _instances = set()
    def __init__(self, thing, name, callback=None):
        self.thing = thing
        self.name = name
        if callback is not None:
            self.add(callback)
        self._instances.add(weakref.ref(self))
    def add(self, callback):
        #Callback provided, special treatment
        self.callback = callback
    def Activate(self):
        #Add Event Detection on self.thing
        print ('Added ' + self.name)
    @classmethod
    def listComponents(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                #print (obj) #Debugging
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead
        
def callback():
    #Do something on Event Detection from thing
    print ('Something happened here')
    
component1 = System('Some', 'C1')
component2 = System('Any', 'C2', callback)
component3 = System('Some', 'C3')
component4 = System('Any', 'C4', callback)
component5 = System('Some', 'C5')
component6 = System('Any', 'C6', callback)

for obj in System.listComponents():
    obj.Activate()