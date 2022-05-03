import RPi.GPIO as GPIO
import time

clockwisePWM = 12
counterclockwisePWM = 13

freq = 500

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(clockwisePWM, GPIO.OUT)
GPIO.setup(counterclockwisePWM, GPIO.OUT)

CW_pwm = GPIO.PWM(clockwisePWM, freq)
CCW_pwm = GPIO.PWM(counterclockwisePWM, freq)
CW_pwm.start(0)
CCW_pwm.start(0)

while True:
    '''for duty in range(0, 101, 1):
        pi_pwm.ChangeDutyCycle(duty)  # provide duty cycle in the range 0-100
        time.sleep(0.01)
    sleep(0.5)

    for duty in range(100, -1, -1):
        pi_pwm.ChangeDutyCycle(duty)
        sleep(0.01)
    time.sleep(0.5)'''
    CW_pwm.ChangeDutyCycle(0)
    CCW_pwm.ChangeDutyCycle(0)

