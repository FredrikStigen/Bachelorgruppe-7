import time
import RPi.GPIO as GPIO

Kp = 0.2
Ki = 0.7
Kd = 0.0025

fs = 235                        #Frequency
Ts = 1/fs                       #Sample period

A = Kp + (0.5*Ki*Ts) + (Kd/Ts)
B = (0.5*Ki*Ts) - (Kd/Ts)
C = Ki

INT_prev = 0.0

e = 0.0                         #Error
e_prev = 0.0                    #Previous error
x_n = 0.0                       #PID output
theta = 0.0                     #Desfired position
theta_fb = 0.0                  #Feedback position
temp = 20                       #Initial temp before reading so theta == 0

INTERVAL = 4000                 #Time interval

EncoderA = 23                   #encoder channel A
EncoderB = 24                   #encoder channel B

n = 0                           #Encoder A pulse

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(EncoderA, GPIO.IN, pull_up_down=GPIO.PUD_up)
GPIO.setup(EncoderB, GPIO.IN)

pulsen = 0

def changeSense(channel, pulsen):
    if GPIO.input(EncoderB):
        if pulsen >= 360:
            pulsen = 0
        pulsen += 1
    else:
        if pulsen <= 0:
            pulsen = 360
        pulsen -= 1
    return pulsen

GPIO.add_event_detect(EncoderA, GPIO.BOTH, callback=changeSense)

while True:



    lastReading = 0             #Static?

    if time.time() >= lastReading + INTERVAL:
        lastReading = time.time()



    #PID Controller
    Ts_prev = 0                 #Static
    if time.time() >= Ts_prev + Ts*1000:        #Ts*1000 to get ms, Ts is in seconds
        Ts_prev = time.time()
        e = theta - theta_fb

        x_n = (A*e) + (B*e_prev) + (C*INT_prev) #PID output calculation

        if x_n >= 12:
            x_n = 12
        elif x_n <= -12:
            x_n = -12

        INT_prev += (0.5*(e + e_prev)*Ts)
        e_prev = e

        u_pwm = abs(x_n) * 21.25

        #Motor direction
        if x_n  < 0:
            GPIO.output(MotorPin1, 1)
            GPIO.output(MotorPin2, 0)
        else:
            GPIO.output(MotorPin1, 0)
            GPIO.output(MotorPin2, 1)