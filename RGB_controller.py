# !/usr/bin/env/python3
#Author: Emilio Axel Sánchez Corona

import time
import RPi.GPIO as GPIO
from random import getrandbits

class RGB:
    
    def __init__(self, pinR, pinG, pinB):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.__pins = [pinR, pinG, pinB]
        GPIO.setup(self.__pins, GPIO.OUT)
        self.__ledr = GPIO.PWM(pinR, 100)
        self.__ledg = GPIO.PWM(pinG, 100)
        self.__ledb = GPIO.PWM(pinB, 100)
        self.__redvalue = 100
        self.__greenvalue = 100
        self.__bluevalue = 100
        self.__brightness = 1
        self.__on = False
        self.__mode = 'solid'
        self.__stop = False
        self.__delay = 0.008
        self.__id = getrandbits(128)
        self.updateColour()
    
    def deleteRGB(self):
        self.__stop = True
        self.__ledr.stop()
        self.__ledg.stop()
        self.__ledb.stop()
        GPIO.cleanup(self.__pins)
        return self

    def changeState(self):
        if self.__on == False:
            self.__on = True
            self.updateColour()
        else:
            self.__on = False
            self.updateColour()
    
    def updateColour(self):
        if self.__on == True:
            self.__ledr.start(self.__redvalue * self.__brightness)
            self.__ledg.start(self.__greenvalue * self.__brightness)
            self.__ledb.start(self.__bluevalue * self.__brightness)
        else:
            self.__ledr.start(0)
            self.__ledg.start(0)
            self.__ledb.start(0)

    def setColour(self, red = 100, green = 100, blue = 100):
        self.__redvalue = red
        self.__greenvalue = green
        self.__bluevalue = blue
        self.updateColour()
    
    def setBrightness(self, brightness = 100):
        self.__brightness = brightness / 100
        self.updateColour()

    def rainbow(self, rstart = 100, gstart = 0, bstart = 0):
        if self.__mode != 'rainbow':
            self.__mode = 'rainbow'
            self.__redvalue = rstart
            self.__greenvalue = gstart
            self.__bluevalue = bstart
        else:
            self.updateColour()
            if 50 < self.__redvalue <= 100 and 0 <= self.__greenvalue <= 50 and self.__bluevalue == 0:
                self.__redvalue -= 1
                self.__greenvalue += 1
                self.__bluevalue = 0
            elif 0 < self.__redvalue <= 50 and 50 <= self.__greenvalue <= 100 and self.__bluevalue == 0:
                self.__redvalue -= 1
                self.__greenvalue += 1
                self.__bluevalue = 0
            elif 50 < self.__greenvalue <= 100 and 0 <= self.__bluevalue <= 50 and self.__redvalue == 0:
                self.__greenvalue -= 1
                self.__bluevalue += 1
                self.__redvalue = 0
            elif 0 < self.__greenvalue <= 50 and 50 <= self.__bluevalue <= 100 and self.__redvalue == 0:
                self.__greenvalue -= 1
                self.__bluevalue += 1
                self.__redvalue = 0
            elif 50 < self.__bluevalue <= 100 and 0 <= self.__redvalue <= 50 and self.__greenvalue == 0:
                self.__bluevalue -= 1
                self.__redvalue += 1
                self.__greenvalue = 0
            elif 0 < self.__bluevalue <= 50 and 50 <= self.__redvalue <= 100 and self.__greenvalue == 0:
                self.__bluevalue -= 1
                self.__redvalue += 1
                self.__greenvalue = 0

    def startLed(self):
        while not self.__stop:
            if self.__mode == 'solid':
                self.updateColour()
            elif self.__mode == 'rainbow':
                self.rainbow()
                time.sleep(self.__delay)
        self.__on = False
        self.updateColour()

    def setDelay(self, delay=.008):
        self.__delay = delay

    def setMode(self, mode='static'):
        self.__mode = mode
    
    @property
    def currentColoursHEX(self):
        return "#{:02x}{:02x}{:02x}".format(round(self.__redvalue * 255 / 100), round(self.__greenvalue * 255 / 100), round(self.__bluevalue * 255 / 100))

    @property
    def currentColoursRGB(self):
        return self.__redvalue, self.__greenvalue, self.__bluevalue
    
    @property
    def currentState(self):
        return self.__on

    @property
    def timing(self):
        return self.__delay

    @property
    def getId(self):
        return self.__id

"""
led1 = RGB(18,13,12)
led2 = RGB(23,19,16)
led1.changeState()
led2.changeState()

while True:
    try:
        led1.rainbow(50,0,50)
        led2.rainbow()
        #print(led1.currentColours)
        time.sleep(.008)
        
    except KeyboardInterrupt:
        break
"""