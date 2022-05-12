import time
import RPi.GPIO as GPIO

sigA = 5
sigB = 6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#GPIO.setup(sigA, GPIO.IN)
GPIO.setup(sigA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sigB, GPIO.IN)

pos = 0


def callback(x):
    global pos
    pos = pos + 1


try:
    GPIO.add_event_detect(sigA, GPIO.RISING, callback=callback, bouncetime=)
    while True:
        print("Channel A: ", GPIO.input(sigA), "Channel B: ", GPIO.input(sigB), "Pos: ", pos)
except KeyboardInterrupt:
    print("Stopped")
