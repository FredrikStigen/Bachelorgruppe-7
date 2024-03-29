import grpc
import proto_pb2
import proto_pb2_grpc
from concurrent import futures
import struct
import sys
import threading
import numpy as np
import pigpio
import RPi.GPIO as GPIO
import time
import Motion_Profile_AtoB_Test

SERVER_ADDRESS = 'localhost:9999'
PIADDRESS = '169.254.165.33:9999'
runTimeBool = False

encoderFeedback = 0
clockwise = True
fposV = []      #
thetaV = []     #Lists for data logging

joystickrun = False
clkwise = True
def changeJoydir(val):
    global clkwise
    if val < 0:
        clkwise = False
    else:
        clkwise = True

def dir(theta, theta_fb):
    global clockwise
    if (theta - theta_fb + 360) % 360 <= 180:
        clockwise = True
    else:
        clockwise = False


########################################
#Corrects the error to find the shortest distance
#########################################
def errorCorrection(theta, theta_fb):
    e = theta - theta_fb
    if abs(e) > 180:
        e = 360 - abs(e)
    return abs(round(e, 3))


#################################################
#Callback function which is run each time an update is detected
#on a channel from the Encoder.
def callback(way):
    global encoderFeedback
    encoderFeedback += way
    if encoderFeedback >= 360:
        encoderFeedback = encoderFeedback - 360
    elif encoderFeedback < -0.001:
        encoderFeedback = encoderFeedback + 360



########################
    #Oppsett av PWM signaler
    ########################


#######################################
#Function that runs the PID controller
#######################################
def controller(vel, acc, variable1, variable2, id):
    global runTimeBool, clockwise, fpos, e
    global encoderFeedback
    global fposV
    global thetaV
    global joystickrun
    global clkwise

    clockwisePWM = 22
    counterclockwisePWM = 27

    freq = 40

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(clockwisePWM, GPIO.OUT)
    GPIO.setup(counterclockwisePWM, GPIO.OUT)

    CW_pwm = GPIO.PWM(clockwisePWM, freq)
    CCW_pwm = GPIO.PWM(counterclockwisePWM, freq)
    CW_pwm.start(0)
    CCW_pwm.start(0)


    class decoder:
        # Class constructor for the encoder, defining the Pi,
        # encoder channel A dn B and a callback function.
        def __init__(self, pi, gpioA, gpioB, callback):
            #Defines the object
            self.pi = pi
            self.gpioA = gpioA
            self.gpioB = gpioB
            self.callback = callback

            #Defines a default level for Channel A and B
            #This part will be used as a debouncer,
            #to eliminate noise that might give false values
            #from the encoder
            self.levA = 0
            self.levB = 0
            self.lastGpio = None


            #Setup for the A and B channels as inputs and interrupts.
            self.pi.set_mode(gpioA, pigpio.INPUT)
            self.pi.set_mode(gpioA, pigpio.INPUT)

            self.pi.set_pull_up_down(gpioA, pigpio.PUD_UP)
            self.pi.set_pull_up_down(gpioB, pigpio.PUD_UP)

            self.cbA = self.pi.callback(gpioA, pigpio.EITHER_EDGE, self._pulse)
            self.cbB = self.pi.callback(gpioB, pigpio.EITHER_EDGE, self._pulse)

        #This function is responsible for calling a callback function,
        #which is used to increase the counter for the position variable.
        #Here we will also eliminate the noise, with the use of a debouncer
        def _pulse(self, gpio, level, tick):
            if gpio == self.gpioA:
                self.levA = level
            else:
                self.levB = level

            if gpio != self.lastGpio:
                self.lastGpio = gpio
                if gpio == self.gpioA and level == 1:
                    if self.levB == 1:
                        self.callback(0.9)
                elif gpio == self.gpioB and level == 1:
                    if self.levA == 1:
                        self.callback(-0.9)


        def cancel(self):
            self.cbA.cancel()
            self.cbB.cancel()

    #######################
    #Kjører motion profilen
    #######################
    if id == 123:
        fpos = Motion_Profile_AtoB_Test.motionProfile(np.radians(vel), acc, np.radians(variable1),
                                                      np.radians(encoderFeedback))
    if id == 456:
        fpos = Motion_Profile_AtoB_Test.motionProfile(np.radians(vel), acc, np.radians(variable2),
                                                      np.radians(variable1))
    if id == 789:
        print(variable1, variable2)
        if encoderFeedback + variable1 > 360:
            fpos = Motion_Profile_AtoB_Test.motionProfile(np.radians(vel), acc,
                                                          np.radians(encoderFeedback + variable1 - 360),
                                                          np.radians(encoderFeedback))
        elif encoderFeedback + variable1 < 0:
            fpos = Motion_Profile_AtoB_Test.motionProfile(np.radians(vel), acc,
                                                          np.radians(encoderFeedback + variable1 + 360),
                                                          np.radians(encoderFeedback))
        else:
            fpos = Motion_Profile_AtoB_Test.motionProfile(np.radians(vel), acc,
                                                          np.radians(encoderFeedback + variable1),
                                                          np.radians(encoderFeedback))




    pi = pigpio.pi()
    decoder = decoder(pi, 5, 6, callback)

    #########################################
    Kp = 10.75                                 #3
    Ki = 0.1                                  #0.01
    Kd = 0                                  #
                                            #
    fs = 4000                               #
    Ts = 1/fs                               #
                                            # Control inputs for the PID controller
    A = Kp + (0.5 * Ki * Ts) + (Kd / Ts)    #
    B = (0.5 * Ki * Ts) - (Kd / Ts)         #
    C = Ki                                  #
                                            #
    INT_prev = 0.0                          #
                                            #
    e_prev = 0.0                            #
    x_n = 0.0                               #
    theta = 90.0                            #
    T = 1/fs                                #
#############################################

    time_prev = time.time()
    time_start = time.time()
    printNow = time.time()
    printDelay = 0.1

    timerStart = time.time()
    print("PID bool {} - Joy bool {}".format(runTimeBool, joystickrun))
    p = 0
    #Runtime for the PID controller
    while runTimeBool:
        theta_fb = encoderFeedback
        Ts_prev = 0

        ####################################
        #How often a new theta value shall be changed
        if time.time() >= time_prev + 0.001:
            time_prev = time.time()
            if p > len(fpos) - 1:
                theta = fpos[len(fpos) - 1]
            else:
                theta = fpos[p]
            p += 1
            fposV.append(round(theta, 3))
            thetaV.append(round(theta_fb, 3))

        ##########################################
        #How often a new x_n value shall be sent adjusted
        ##########################################
        if time.time() >= Ts_prev + 0.05:
            Ts_prev = time.time()
            e = errorCorrection(theta, theta_fb)        #Corrects the error to find the shortest distance

            x_n = (A * e) + (B * e_prev) + (C * INT_prev)
            if fpos[-1] + 0.5 >= theta_fb >= fpos[-1] - 0.5:
                x_n = 0
                INT_prev = 0
                if id == 456:                   #Flips the motion profile when the prototype is set to rotate
                    fpos = np.flip(fpos)        #between two positions
                    if clockwise:
                        clockwise = False
                    else:
                        clockwise = True
                elif id == 789:                 #What motion profile that will be generated for this specific operation
                    CCW_pwm.ChangeDutyCycle(0)  # 0 to counterclockwise PWM port
                    CW_pwm.ChangeDutyCycle(0)
                    if time.time() >= printNow + printDelay:
                        printNow = time.time()
                        print("Theta: ", round(theta, 2), "Theta_fb: ", round(theta_fb, 2), "e: ", round(e, 2),
                              "clockwise: ",
                              clockwise, "x_n: ", round(x_n, 2))
                    time.sleep(variable2)
                    if encoderFeedback + variable1 > 360:
                        fpos = Motion_Profile_AtoB_Test.motionProfile(np.radians(vel), acc,
                                                                      np.radians(encoderFeedback + variable1 - 360),
                                                                      np.radians(encoderFeedback))
                    elif encoderFeedback + variable1 < 0:
                        fpos = Motion_Profile_AtoB_Test.motionProfile(np.radians(vel), acc,
                                                                      np.radians(encoderFeedback + variable1 + 360),
                                                                      np.radians(encoderFeedback))
                    else:
                        fpos = Motion_Profile_AtoB_Test.motionProfile(np.radians(vel), acc,
                                                                      np.radians(encoderFeedback + variable1),
                                                                      np.radians(encoderFeedback))


            INT_prev += (0.5 * (e + e_prev) * Ts)
            e_prev = e

            dir(theta, theta_fb)        #Set the correct direction

        if x_n > 100:       #If x_n value goes above 100 it will be defined as 100
            x_n = 100

        if x_n < 0:         #If x_n value goes below 0 it will be defined as 0
            x_n = 0

        if 0 < x_n < 10:
            x_n = 10

        if clockwise:
            CCW_pwm.ChangeDutyCycle(0)          #0 to counterclockwise PWM port
            CW_pwm.ChangeDutyCycle(x_n)         #x_n value is sent to clockwise PWM port
        else:
            CW_pwm.ChangeDutyCycle(0)           #0 to clockwise PWm port
            CCW_pwm.ChangeDutyCycle(x_n)        #x-N value is sent to clockwise PWM port

        ###############################################
        #Print of different values to analyze and debug
        if time.time() >= printNow + printDelay:
            printNow = time.time()
            print("Theta: ", round(theta, 2), "Theta_fb: ", round(theta_fb, 2), "e: ", round(e, 2), "clockwise: ",
                  clockwise, "x_n: ", round(x_n, 2))

    infile_path = "/dev/input/event" + (sys.argv[1] if len(sys.argv) > 1 else "0")

    FORMAT = 'llHHI'
    EVENT_SIZE = struct.calcsize(FORMAT)

    # open file in binary mode
    in_file = open(infile_path, "rb")

    event = in_file.read(EVENT_SIZE)
    while event and joystickrun and id == 1111:
        #global clkwise
        (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)
        if type != 0 or code != 0 or value != 0:
            # print("Event type %u, code %u, value %u at %d.%d" % \
            # (type, code, value, tv_sec, tv_usec))
            if code == 0:
                value -= 8200
                value = round(value / 82)
                print(value)
                changeJoydir(value)
                print("Direction: {} - Value: {}".format(clkwise, value))
                if clkwise:
                    CCW_pwm.ChangeDutyCycle(0)
                    CW_pwm.ChangeDutyCycle(value)
                else:
                    CW_pwm.ChangeDutyCycle(0)
                    CCW_pwm.ChangeDutyCycle(abs(value))

        event = in_file.read(EVENT_SIZE)


    in_file.close()
    CCW_pwm.ChangeDutyCycle(0)
    CW_pwm.ChangeDutyCycle(0)




    #Simple code to log data from encoder feedback and position from motions profile.
    with open('fposlog.txt', 'w') as filehandler:
        for listitem in fposV:
            filehandler.write('%s\n' % listitem)
    with open('thetafblog.txt', 'w') as filehandler:
        for listitem in thetaV:
            filehandler.write('%s\n' % listitem)
    print("Stopped")
    timerStop = time.time()
    print("Seconds elapsed: {}".format(round(timerStop - timerStart, 2)))
    CW_pwm.stop()
    CCW_pwm.stop()
    pi.cleanup()









#Class for the communication channel, with the implementation of a thread that starts
#the PID controller
class ComChan(proto_pb2_grpc.streamServicer):
    def SM(self, request, context):
        global runTimeBool
        global joystickrun
        print("Method called by client")
        PID = threading.Thread(target=controller, args=(request.velocity,
                                                        request.acceleration,
                                                        request.variable1,
                                                        request.variable2,
                                                        request.methodID))
        if request.run:
            if request.methodID == 1111:
                joystickrun = request.run
            elif request.methodID == 123 or request.methodID == 456 or request.methodID == 789:
                runTimeBool = request.run
            PID.start()
        else:
            runTimeBool = request.run
            joystickrun = request.run


        run = 4
        data = encoderFeedback
        response = proto_pb2.serverResponse(runTime=run, eData=round(data))
        return response


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    proto_pb2_grpc.add_streamServicer_to_server(ComChan(), server)
    server.add_insecure_port(PIADDRESS)

    print("Server is running...")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Stopped by interrupt")