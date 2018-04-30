#!/usr/bin/python
import RPi.GPIO as GPIO
from datetime import *
import time
import sys
import random
import http.client

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

trig = 23
echo = 24

offset = round (0.6, 2)
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)


total_level = int(input('enter initial level\n'))
    
while True:
                             
    GPIO.output(trig, False)                #print(' Sensor initialize ')
    time.sleep(2)

    GPIO.output(trig, True)                  #print('pulses (trigger)')
    time.sleep(0.00001)
    GPIO.output(trig, False)

    while GPIO.input(echo)==0:
        pulse_begin = time.time()
    while GPIO.input(echo)==1:
        pulse_end = time.time()
    pulse_width = pulse_end - pulse_begin

    calculated_level = pulse_width * 17150
    
    garbage_level = round(total_level - calculated_level, 1)
	
    percent_level = (float(garbage_level) / float(total_level))
    percent_level = percent_level*100

    connect = http.client.HTTPConnection('172.16.8.135:8000')
    connect.request('GET', '/api/1/' + str(percent_level) + '/')
    
    time.sleep(60)
GPIO.cleanup()
print("Done\n")
