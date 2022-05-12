import RPi.GPIO as GPIO

clockwisePWM = 12
counterclockwisePWM = 13

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
    while True:
        CW_pwm.ChangeDutyCycle(75)
        CCW_pwm.ChangeDutyCycle(0)
except KeyboardInterrupt:
    CW_pwm.stop()
    CCW_pwm.stop()



'''def running(run):
    while run:
        CW_pwm.ChangeDutyCycle(75)
        CCW_pwm.ChangeDutyCycle(0)

    if run == False:
        CW_pwm.stop()
        CCW_pwm.stop()
        print("PWM stopped")'''