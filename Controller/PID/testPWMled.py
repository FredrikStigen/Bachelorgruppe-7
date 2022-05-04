import RPi.GPIO as GPIO
import time

ledpin = 12
ledpin2 = 13# PWM pin connected to LED
GPIO.setwarnings(False)  # disable warnings
GPIO.setmode(GPIO.BCM)  # set pin numbering system
GPIO.setup(ledpin, GPIO.OUT)
GPIO.setup(ledpin2, GPIO.OUT)
pi_pwm = GPIO.PWM(ledpin, 1000)
pi_pwm2 = GPIO.PWM(ledpin2, 1000)# create PWM instance with frequency
pi_pwm.start(0)
pi_pwm2.start(0)# start PWM of required Duty Cycle
try:
    while True:
        for duty in range(0, 101, 1):
            pi_pwm.ChangeDutyCycle(duty)
            pi_pwm2.ChangeDutyCycle(duty)# provide duty cycle in the range 0-100
            time.sleep(0.01)
        time.sleep(0.5)

        for duty in range(100, -1, -1):
            pi_pwm.ChangeDutyCycle(duty)
            pi_pwm2.ChangeDutyCycle(duty)
            time.sleep(0.01)
        time.sleep(0.5)
        '''GPIO.output(ledpin, 1)
        time.sleep(0.5)
        GPIO.output(ledpin, 0)
        time.sleep(0.5)'''

except KeyboardInterrupt:
    pass
pi_pwm.stop()
pi_pwm2.stop()
GPIO.cleanup()