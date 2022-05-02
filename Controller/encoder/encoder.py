import time
import RPi.GPIO as GPIO

sigA = 5
sigB = 6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(sigA, GPIO.IN)
GPIO.setup(sigB, GPIO.IN)


while True:
	print("sigA: ", GPIO.input(sigA))
	print("sigB: ", GPIO.input(sigB))
	time.sleep(0.01);
