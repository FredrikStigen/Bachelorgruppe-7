import struct
import time
import sys
import RPi.GPIO as GPIO

infile_path = "/dev/input/event" + (sys.argv[1] if len(sys.argv) > 1 else "2")

FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

#open file in binary mode
in_file = open(infile_path, "rb")

event = in_file.read(EVENT_SIZE)

clockwise = True

def changeDirection(val):
    global clockwise
    if val < 0:
        clockwise = False
    else:
        clockwise = True
        
        
clockwisePWM = 22
counterclockwisePWM = 27

freq = 40

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(clockwisePWM, GPIO.OUT)
GPIO.setup(counterclockwisePWM, GPIO.OUT)

CW_pwm = GPIO.PWM(clockwisePWM, freq)
CCW_pwm = GPIO.PWM(counterclockwisePWM, freq)
CW_pwm.start(0)
CCW_pwm.start(0)

try:
    while event:
        (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

        if type != 0 or code != 0 or value != 0:
            #print("Event type %u, code %u, value %u at %d.%d" % \
                #(type, code, value, tv_sec, tv_usec))
            if code == 0:
                value -= 8200
                value = round(value / 82)
                changeDirection(value)
                print("Direction: {} - Value: {}".format(clockwise, value))
                if clockwise:
                    CCW_pwm.ChangeDutyCycle(0)
                    CW_pwm.ChangeDutyCycle(value)
                else:
                    CW_pwm.ChangeDutyCycle(0)
                    CCW_pwm.ChangeDutyCycle(abs(value))
            if code == 6:
                freq = value
                print("Hz changed to: {}".format(freq))

        event = in_file.read(EVENT_SIZE)
except KeyboardInterrupt:
    in_file.close()
