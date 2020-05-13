# !/usr/bin/env/python3
#Author: Emilio Axel Sánchez Corona
import os
from time import sleep
import signal
import sys
import RPi.GPIO as GPIO

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

def getCPUtemp():
    res = os.popen('vcgencmd measure_temp').readline()
    temp = (res.replace("temp=","").replace("'C\n",""))
    return float(temp)

def fanon():
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, 1)
    return True

def fanoff():
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, 0)
    return False

def main():
    setup()
    fan = fanon()
    sleep(10)
    fan = False
    while True:
        temp = getCPUtemp()
        if temp >= 53:
            fan = fanon()
        elif temp <= 37 and fan == True:
            fan = fanoff()
        elif temp <53 and fan == False:
            fan = fanoff()
        sleep(3)

main()