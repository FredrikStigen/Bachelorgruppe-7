import time
import RPi.GPIO as GPIO

sigA = 5
sigB = 6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(sigA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sigB, GPIO.IN)

pos = 0
def callback(channel):
	global pos
	pos += 1
	print("test")


try:
	#GPIO.add_event_detect(sigA, GPIO.FALLING, callback=callback)
	GPIO.add_interrupt_callback(sigA, callback, edge='both',
								pull_up_down=GPIO.PUD_OFF, threaded_callback=False, debounce_timeout_ms=None)
	while True:
		print("sigA: ", GPIO.input(sigA), "sigB: ", GPIO.input(sigB), "Pos: ", pos)
except KeyboardInterrupt:
	print("Stopped")