import time
import RPi.GPIO as GPIO
from encoder import Encoder

def valueChanged(value, direction):
    print("* New value: {}, Direction: {}".format(value, direction))

GPIO.setmode(GPIO.BCM)

e1 = Encoder(5, 6, valueChanged)

try:
    while True:
        time.sleep(5)
        print("Value is {}".format(e1.getValue()))
except KeyboardInterrupt:
    pass

GPIO.cleanup()