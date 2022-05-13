import RPi.GPIO as GPIO
import time

clockwisePWM = 22
counterclockwisePWM = 27

freq = 2000

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(clockwisePWM, GPIO.OUT)
GPIO.setup(counterclockwisePWM, GPIO.OUT)

CW_pwm = GPIO.PWM(clockwisePWM, freq)
CCW_pwm = GPIO.PWM(counterclockwisePWM, freq)
CW_pwm.start(0)
CCW_pwm.start(0)
try:
    while True:
        CW_pwm.ChangeDutyCycle(0)
        CCW_pwm.ChangeDutyCycle(0)
except KeyboardInterrupt:
        pass
CW_pwm.stop()
CCW_pwm.stop()
#GPIO.cleanup()