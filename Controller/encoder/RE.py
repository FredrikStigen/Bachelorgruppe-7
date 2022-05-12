import pigpio
import time

pinA = 5
pinB = 6

pos = 0

def callback(gpio, level, tick):
   global pos
   pos += 1


pi = pigpio.pi()
#pi.set_mode(pinA, pigpio.INPUT)
pi.set_mode(pinB, pigpio.INPUT)

pi.set_pull_up_down(pinA, pigpio.PUD_UP)

pi.callback(pinA, pigpio.FALLING_EDGE, callback)



try:
   while True:
      print("Channel A: ", pi.read(pinA), "Channel B: ", pi.read(pinB), "Pos: ", pos)
      #time.sleep(1)
except KeyboardInterrupt:
   print("Stopped")
   pi.stop()





'''class decoder:
    def __init__(self, pi, ChanA, callback):
        self.pi = pi
        self.ChanA = ChanA
        self.callback = callback

        self.levelA = 0
        self.levelB = 0

        self.pi.set_pull_up_down(ChanA, pigpio.PUD_UP)

        self.cbA = self.pi.callback(ChanA, pigpio.RISING_EDGE, self.callback)


pos = 0
def callback():
   global pos
   pos += 1
   
try:
   pi = pigpio.pi()
   decoder = decoder(pi, 5, callback)
   while True:
      print(decoder.ChanA)
except KeyboardInterrupt:
   pi.stop()'''