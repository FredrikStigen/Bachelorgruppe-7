import pigpio
import time
import RPi.GPIO as GPIO


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
               self.callback(0.9)
         elif gpio == self.gpioB and level == 1:
            if self.levA == 1:
               self.callback(-0.9)

   def cancel(self):
      self.cbA.cancel()
      self.cbB.cancel()


f = open("position.txt", "r")
encoderFeedback = float(f.read())
f.close()

def callback(way):
   global encoderFeedback
   if encoderFeedback >= 360:
      encoderFeedback = 0
   elif encoderFeedback <= 0:
      encoderFeedback = 360
   encoderFeedback += way




Kp = 0.2
Ki = 0.7
Kd = 0.0025

fs = 235                        #Frequency
Ts = 1/fs                       #Sample period

A = Kp + (0.5*Ki*Ts) + (Kd/Ts)
B = (0.5*Ki*Ts) - (Kd/Ts)
C = Ki

INT_prev = 0.0

#e = 0.0                         #Error
e_prev = 0.0                    #Previous error
x_n = 0.0                       #PID output
theta = 90.0                     #Desfired position
#theta_fb = 360      #Feedback position

clockwise = True                  #Defines the direction of the motor

def dir(theta, theta_fb):
   global clockwise
   if ((theta - theta_fb + 360) % 360 <= 180):
      clockwise = True
   else:
      clockwise = False


def errorCorrection(theta, theta_fb):
   e = theta - theta_fb
   if abs(e) > 180:
      e = 360 - abs(e)
   return abs(round(e, 3))


if __name__ == "__main__":
   pi = pigpio.pi()

   decoder = decoder(pi, 5, 6, callback)
   while True:
      theta_fb = round(encoderFeedback, 3)
      f = open("position.txt", "w")
      f.write("{}".format(theta_fb))
      f.close()

      Ts_prev = 0  # Static
      if time.time() >= Ts_prev + Ts * 1000:  # Ts*1000 to get ms, Ts is in seconds
         Ts_prev = time.time()

         #e = theta - theta_fb
         e = errorCorrection(theta, theta_fb)

         x_n = (A * e) + (B * e_prev) + (C * INT_prev)  # PID output calculation


         INT_prev += (0.5 * (e + e_prev) * Ts)
         e_prev = e

         dir(theta, theta_fb)

         print("Theta: ", theta, "Theta_fb: ", theta_fb, "e: ", e, "clockwise: ", clockwise)


      time.sleep(1) # fjern etter testing


      #print("pos = {}".format(round(encoderFeedback * 0.9, 3)))

decoder.cancel()

pi.stop()
