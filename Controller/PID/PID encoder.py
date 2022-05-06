import pigpio
import time
import numpy as np
import RPi.GPIO as GPIO
import Motion_Profile_AtoB_Test

####################################################
#Klasse for Raspberry Pi for definering av encoder
class decoder:
   def __init__(self, pi, gpioA, gpioB, callback):

      self.pi = pi
      self.gpioA = gpioA
      self.gpioB = gpioB
      self.callback = callback

      self.levA = 0
      self.levB = 0

      self.lastGpio = None

      self.pi.set_mode(gpioA, pigpio.INPUT)
      self.pi.set_mode(gpioB, pigpio.INPUT)

      self.pi.set_pull_up_down(gpioA, pigpio.PUD_UP)
      self.pi.set_pull_up_down(gpioB, pigpio.PUD_UP)

      self.cbA = self.pi.callback(gpioA, pigpio.EITHER_EDGE, self._pulse)
      self.cbB = self.pi.callback(gpioB, pigpio.EITHER_EDGE, self._pulse)

   def _pulse(self, gpio, level, tick):
      if gpio == self.gpioA:
         self.levA = level
      else:
         self.levB = level;

      if gpio != self.lastGpio: # debounce
         self.lastGpio = gpio

         if   gpio == self.gpioA and level == 1:
            if self.levB == 1:
               self.callback(1)
         elif gpio == self.gpioB and level == 1:
            if self.levA == 1:
               self.callback(-1)

   def cancel(self):
      self.cbA.cancel()
      self.cbB.cancel()
##############################################################

######################
#Definere position
encoderFeedback = 0
######################

################################
#Encoder interrupt
def callback(way):
   global encoderFeedback
   if encoderFeedback >= 400:
      encoderFeedback = 0
   elif encoderFeedback <= 0:
      encoderFeedback = 400
   encoderFeedback += way
################################



Kp = 3
Ki = 0.01
Kd = 0.0

fs = 1000                        #Frequency
Ts = 1/fs                       #Sample period
A = Kp + (0.5*Ki*Ts) + (Kd/Ts)
B = (0.5*Ki*Ts) - (Kd/Ts)
C = Ki
INT_prev = 0.0
e_prev = 0.0                    #Previous error
x_n = 0.0                       #PID output
theta = 90.0                     #Desfired position
T = 1/fs                   #Samplid tid i motion profil

clockwise = True                  #Defines the direction of the motor

###############################################
#Definerer hvilken retning systemet skal rotere
def dir(theta, theta_fb):
   global clockwise
   if ((theta - theta_fb + 360) % 360 <= 180):
      clockwise = True
   else:
      clockwise = False
###############################################

#####################################
#Korrigerer error for å finne korteste vei
def errorCorrection(theta, theta_fb):
   e = theta - theta_fb
   if abs(e) > 180:
      e = 360 - abs(e)
   return abs(round(e, 3))
#####################################

####################################################################
#Generering av motion profil vector
fpos = Motion_Profile_AtoB_Test.motionProfile(3*np.pi/2, 6, np.pi/2)
####################################################################
#for i in range(len(fpos)):
   #print(fpos[i])

timeLast = time.time()
delay = 0.001
increment = 0

#####################################################
#Oppset av PWM
clockwisePWM = 12
counterclockwisePWM = 13

freq = 1000

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(clockwisePWM, GPIO.OUT)
GPIO.setup(counterclockwisePWM, GPIO.OUT)

CW_pwm = GPIO.PWM(clockwisePWM, freq)
CCW_pwm = GPIO.PWM(counterclockwisePWM, freq)
CW_pwm.start(0)
CCW_pwm.start(0)
####################################################

try:
   pi = pigpio.pi()

   decoder = decoder(pi, 5, 6, callback)
   time_prev = time.time()
   time_start = time.time()

   printNow = time.time()
   printDelay = 0.1
   while True:
      theta_fb = round(encoderFeedback * 0.9, 3)
      Ts_prev = 0  # Static

      ################################################################
      #Hvor ofte nye posisjoner skal sendes ut fra motion profilen
      if time.time() <= time_prev + 0.001:
         time_prev = time.time()
         i = round((time_prev - time_start) / T)
         if i > len(fpos)-1:
            theta = fpos[len(fpos)-1]
         else:
            theta = fpos[i]
      ################################################################

      ################################################################
      #Hvor ofte nye x_n verdier skal bli endret
      if time.time() >= Ts_prev + 0.00025:
         Ts_prev = time.time()
         e = errorCorrection(theta, theta_fb)

         x_n = (A * e) + (B * e_prev) + (C * INT_prev)  # PID output calculation
         if theta_fb <= theta + 0.9 and theta_fb >= theta - 0.9:
            x_n = 0

         INT_prev += (0.5 * (e + e_prev) * Ts)
         e_prev = e

         dir(theta, theta_fb)
      ################################################################

      ################################################################
      #Regulere output'en, slik at x_n aldri går over 100%
      if x_n > 100:
         x_n = 100
      ################################################################

      ################################################################
      #Korrigere hvilken retning motoren skal snurre
      if clockwise == True:
         CW_pwm.ChangeDutyCycle(x_n)
         CCW_pwm.ChangeDutyCycle(0)
      else:
         CW_pwm.ChangeDutyCycle(0)
         CCW_pwm.ChangeDutyCycle(x_n)
      ################################################################
      #Hvor fote en visuel fremstilling av verdier skal printes
      if time.time() >= printNow + printDelay:
         printNow = time.time()
         print("Theta: ", round(theta, 2), "Theta_fb: ", round(theta_fb,2 ), "e: ", round(e, 2), "clockwise: ", clockwise, "x_n: ", x_n)
      ################################################################



except KeyboardInterrupt:
   CW_pwm.ChangeDutyCycle(0)
   CCW_pwm.ChangeDutyCycle(0)

   decoder.cancel()
   pi.stop()
