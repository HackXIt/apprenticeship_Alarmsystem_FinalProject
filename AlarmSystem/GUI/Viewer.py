#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 03:16:04 2017

@author: Nikolaus Rieder
tkinter Testing Environment
Possibly Module for AlarmSystem later on
"""

import tkinter as tk

class Alarmviewer(tk.Frame):
   def __init__(self, parent):
       tk.Frame.__init__(self, parent)
       self.parent = parent
       self.initialize_user_interface()

   def initialize_user_interface(self):
       self.parent.title("Alarmviewer")
       #Initialize Frames
       self.picture = tk.Frame(self.parent)
       self.components = tk.Frame(self.parent)
       self.statusList = tk.Frame(self.parent)
       self.mode = tk.Frame(self.parent)
       self.camera = tk.Frame(self.parent)
       self.picture.grid(row=0, column=0, sticky='nw')
       self.components.grid(row=1, column=1, sticky='w')
       self.statusList.grid(row=1, column=2, sticky='w')
       self.mode.grid(row=2, column=1, sticky='w')
       self.camera.grid(row=3, column=1, sticky='w')
       
       #Frame 1: picture
       self.png = tk.PhotoImage(file='/home/pi/Pictures/example_layout.png')
       self.photoLabel = tk.Label(self.picture, image=self.png)
       self.photoLabel.grid(row=0, column=0, sticky='nw')
       
       #Frame 2: components
       components = ['REED', 'PIR', 'VIBR', 'REED', 'PIR']
       for index, item in enumerate(components):
           component = tk.Label(self.components, text=item)
           component.grid(row=index,column=0)
       #Frame 3: statusList
       statusL = [[True, False, True, False, True],
                ['14:00:00', '13:24:31', '15:58:32', '08:33:01', '07:11:01']]
       for indexList, seq in enumerate(statusL):
           for indexSeq, item in enumerate(seq):
               lastState = tk.Label(self.statusList, text=item)
               lastState.grid(row=indexSeq, column=indexList)
       #Frame 4: mode
       self.switch = tk.Button(self.mode, 
                               text='Arm / Disarm', 
                               command=self.popUp)
       self.switch.grid(row=0, column=0)
       self.check = tk.Label(self.mode, text='')
       self.check.grid(row=0, column=1)
       #Frame 5: camera
       
   def popUp(self):
       self.kid = tk.Toplevel(width=100, height=150)
       self.kid.title('Verification')
       self.kid.geometry('250x50')
       self.entry = tk.Entry(self.kid)
       self.entry.grid(row=0)
       self.confirm = tk.Button(self.kid,
                                fg='black', text='Confirm',
                                command=self.passCheck)
       self.confirm.grid(row=0, column=1)
   def passCheck(self):
       code = self.entry.get()
       print (code)
       if code == '1234':
           self.check.config(text='Success')
           self.kid.destroy()
       else:
           self.check.config(text='Wrong code')
           self.kid.destroy()