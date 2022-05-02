import time
import RPi.GPIO as GPIO

sigA = 5
sigB = 6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(sigA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sigB, GPIO.IN)

counter = 0.0

def changeSense(channel):
	global counter
	if GPIO.input(sigB):
		if counter >= 400:
			counter = 0
		counter += 1
	else:
		if counter <= 0:
			counter = 400
		counter -= 1
	#print(round(counter*0.9, 2))


GPIO.add_event_detect(sigA, GPIO.FALLING, callback=changeSense)


while True:
	time.sleep(0)
	#GPIO.wait_for_edge(sigB, GPIO.FALLING)
