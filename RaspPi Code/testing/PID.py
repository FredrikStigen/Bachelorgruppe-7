#import pigpio
import time
#import RPi.GPIO as GPIO


def PID_Controller(run):
    i = 0
    while run:
        if i >= 100000000:
            print("Loop has run 100 000 000 times")
            run = False
        i += 1