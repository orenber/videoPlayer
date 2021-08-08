import time
from tkinter import *
from datetime import datetime


class Clock:

    def __init__(self,label:Label):
        self.label = label
        self._play = False
        self._hour = "00"
        self._minutes = "00"
        self._sec = "00"
        self._handle = ""

    def get_current_time(self)->str:
        self._hour = time.strftime("%H")
        self._minutes = time.strftime("%M")
        self._sec = time.strftime("%S")
        return  self._hour + ":" + self._minutes + ":" + self._sec

    def run(self):
        if self._play:

            self.label.config(text=self.get_current_time())
            self._handle = self.label.after(1000, lambda: self.run())
        else:
            self.label.after_cancel(self._handle)
            self._handle = None

    def start(self):
        self._play = True
        self.run()

    def stop(self):
        self._play = False


class Stopper(Clock):

    def __init__(self, label:Label):
        super().__init__(label)
        self._FMT = '%H:%M:%S'
        self._initial_time = "00:00:00"

    def get_stopper_time(self)->str:

        tdelta = datetime.strptime(self.get_current_time(), self._FMT) - datetime.strptime(self._initial_time , self._FMT)
        return tdelta

    def run(self):
        if self._play:

            self.label.config(text=self.get_stopper_time())
            self._handle = self.label.after(1000, lambda: self.run())
        else:
            self.label.after_cancel(self._handle)
            self._handle = None

    def start(self):
        self._play = True
        self._initial_time = self.get_current_time()
        self.run()
