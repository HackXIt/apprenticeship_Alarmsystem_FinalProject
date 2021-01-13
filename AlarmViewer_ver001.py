#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 03:16:04 2017

@author: Nikolaus Rieder
tkinter Testing Environment
Possibly Module for AlarmSystem later on
"""

import tkinter as tk
import time

tk.Frame = tk.LabelFrame

class Alarmviewer(tk.Frame):
    componentsL = []
    statusL = []
    statusD = {}
    __code = None
    __status = None
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        Alarmviewer.parent = parent
        self.screen_width = parent.winfo_screenwidth()
        self.screen_height = parent.winfo_screenheight()
        self.startup(400, 40)
        
    def startup(self, width, height):
        self.parent.withdraw() # Hide Main Window
        self.pop = tk.Toplevel() # Create PopUp for setup
        self.pop.title('Setup Code for Verification')
        self.pop.protocol('WM_DELETE_WINDOW', self.pop.destroy)
        x = (self.screen_width/2) - (width/2)
        y = (self.screen_height/2) - (height/2)
        self.pop.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.code = tk.Entry(self.pop)
        self.code.grid(row=0, column=0, ipadx=width-20)
        self.confirm = tk.Button(self.pop,
                                 fg='black', text='Confirm',
                                 command=self._setCode)
        self.confirm.grid(row=0, column=1, ipadx=width-20)
        self.pop.grid_rowconfigure(index=0, weight=1)
        self.pop.grid_columnconfigure(index=0, weight=1)
        self.pop.grid_columnconfigure(index=1, weight=1)
        
    def _setCode(self):
        Alarmviewer.__code = self.code.get()
        self.pop.destroy()
        self.initialize_user_interface()
        
    def initialize_user_interface(self):
        #Configure Main Window
        self.parent.deiconify() # Bring back Main Window
        self.parent.title("Alarmviewer")
        self.parent.protocol('WM_DELETE_WINDOW', self.Cleaner)
        x = self.screen_width/2
        y = self.screen_height/1.5
        self.parent.geometry('%dx%d+%d+%d' % (x, y, 
                                              x/2, y*0.25))
        #Variables   
        #Initialize Frames
        self.sideA = tk.Frame(self.parent, bg='black')
        self.sideB = tk.Frame(self.parent, bg='white')
        self.picture = tk.Frame(self.sideA)
        self.components = tk.Frame(self.sideB, bg='white')
        self.statusList = tk.Frame(self.sideB, bg='white')
        self.buttons = tk.Frame(self.sideB, bg='white')
        self.camera = tk.Frame(self.sideA)
        
        #Positioning in Main Window
        #Frame - sideA
        self.sideA.grid(row=0, column=0)
        self.sideA.grid_columnconfigure(0, weight=2)
        self.picture.grid(row=0, column=0, sticky='nswe')
        self.camera.grid(row=1, column=0, sticky='nswe')
        
        #Widget - picture
        try:
            self.png = tk.PhotoImage(file='/home/pi/Pictures/example_layout.png')
            self.photoLabel = tk.Label(self.picture, image=self.png)
            self.photoLabel.grid(row=0, column=0, sticky='nswe')
        except tk.TclError:
            print ('Image skipped. DEBUG')
        #Widget - camera
        
        #Frame - sideB
        self.sideB.grid(row=0, column=1, sticky='nswe')
        self.sideB.grid_columnconfigure(1, weight=1)
        self.components.grid(row=0, column=0, sticky='w')
        self.statusList.grid(row=0, column=1, sticky='e')
        self.buttons.grid(row=1, columnspan=2, sticky='nw', 
                          ipadx=self.sideB.winfo_reqwidth())
        #Frame - buttons
        #Widget - mode
        self.mode = tk.Button(self.buttons, 
                                text='Start', 
                                command=lambda: self.codeUp(300, 40),
                                width=20)
        self.mode.grid(row=0, column=0)
#        self.arm.grid_rowconfigure(0, weight=1)
        #Widget - Check
        self.check = tk.Label(self.buttons, text=None, bg='white')
        self.check.grid(row=1, columnspan=2, sticky='nw')
    def clearLabels(self):
        tmp = []
        for label in self.components.children.values():
            tmp.append(label)
        for label in self.statusList.children.values():
            tmp.append(label)
        for label in tmp:
            label.destroy()
    @classmethod
    def createList(cls, self):
        #Debug Message
#        print('creating')
        for key, value in self.statusD.items():
            cls.componentsL.append(key)
            cls.statusL.append(value)
        #Configure Frame - components
        for index, item in enumerate(cls.componentsL):
            self.component = tk.Label(self.components, text=item, bg='white',
                                      width=5, anchor='w')
            self.component.grid(row=index, sticky='w')
        #Configure Frame - statusList
        for index, item in enumerate(cls.statusL):
            self.status = tk.Label(self.statusList, text=item, bg='white',
                                   anchor='e')
            self.status.grid(row=index, sticky='e')
    def updateList(self, dictionary):
        #Debug Message
#        print('updating')
                
        self.statusD = dictionary
        #Empty Lists
        self.componentsL.clear()
        self.statusL.clear()
        self.clearLabels()
        
        #Rebuild Lists
        self.createList(self)
        
        #DEBUG
#        self.parent.after(4000, lambda: self.updateList(statusDictionary))
        
    def codeUp(self, width, height):
        self.kid = tk.Toplevel()
        self.kid.title('Verification')
        x = (self.screen_width/2) - (width/2)
        y = (self.screen_height/2) - (height/2)
        self.kid.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.entry = tk.Entry(self.kid)
        self.entry.grid(row=0)
        self.verify = tk.Button(self.kid, bg='green',
                                 fg='black', text='Verify',
                                 command=self.passCheck)
        self.verify.grid(row=0, column=1)
        
    def passCheck(self):
        code = self.entry.get()
        print (code) #DEBUG
        if code == Alarmviewer.__code:
            if self.__status is None:
                Alarmviewer.__status = 'Armed'
                self.mode.config(text='Press to Disarm')
            elif self.__status == 'Armed':
                Alarmviewer.__status = 'Disarmed'
                self.mode.config(text='Press to Arm')
            elif self.__status == 'Disarmed':
                Alarmviewer.__status = 'Armed'
                self.mode.config(text='Press to Disarm')

            self.check.config(text=str('Success - %s' % self.__status))
            self.kid.destroy()
        else:
            self.check.config(text='Wrong code')
            self.kid.destroy()
    @staticmethod
    def getMode():
        return Alarmviewer.__status
    @classmethod
    def Cleaner(cls):
        cls.componentsL.clear()
        cls.statusL.clear()
        cls.parent.destroy()
        cls.parent.quit()
        
#for Window DEBUG
if __name__ == '__main__':
    global statusDictionary
    statusDictionary = {'REED':'2017|11|14 15:32:13', 
                        'PIR':'2017|10|14 13:15:54',
                        'VIBR':'2017|09|16 08:45:10'}
    root = tk.Tk()
    run = Alarmviewer(root)
    root.after(4000, lambda: run.updateList(statusDictionary))
    root.mainloop()