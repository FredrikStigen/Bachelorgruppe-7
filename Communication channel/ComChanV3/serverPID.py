import grpc
import proto_pb2
import proto_pb2_grpc
from concurrent import futures
import threading
import numpy as np
import pigpio
import RPi.GPIO as GPIO
import time
import Motion_Profile_AtoB_Test

SERVER_ADDRESS = 'localhost:9999'
PIADDRESS = '169.254.131.27:9999'
runTimeBool = False

############################
encoderFeedback = 0
#Posisjon på prototyp og hvilken retning den kjører
clockwise = True
############################


def dir(theta, theta_fb):
    global clockwise
    if (theta - theta_fb + 360) % 360 <= 180:
        clockwise = True
    else:
        clockwise = False


########################################
#Korrigerer error for på finne minste vei
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
    if encoderFeedback >= 400:
        encoderFeedback = 0
    elif encoderFeedback <= 0:
        encoderFeedback = 400
    encoderFeedback += way


#######################################
#Funksjon for kjøring av PID controller
#######################################
def controller(vel, acc, pos):
    global runTimeBool
    global encoderFeedback


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
                        self.callback(1)
                elif gpio == self.gpioB and level == 1:
                    if self.levA == 1:
                        self.callback(-1)


        def cancel(self):
            self.cbA.cancel()
            self.cbB.cancel()

    #######################
    #Kjører motion profilen
    #######################
    fpos = Motion_Profile_AtoB_Test.motionProfile(np.radians(vel), acc, np.radians(pos), np.radians(encoderFeedback))

    ########################
    #Oppsett av PWM signaler
    ########################
    clockwisePWM = 18
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

    #######################
    #Definerer Pi og object
    #######################
    pi = pigpio.pi()
    decoder = decoder(pi, 5, 6, callback)

    Kp = 3
    Ki = 0.01
    Kd = 0.0

    fs = 1000
    Ts = 1/fs

    A = Kp + (0.5 * Ki * Ts) + (Kd / Ts)
    B = (0.5 * Ki * Ts) - (Kd / Ts)
    C = Ki

    INT_prev = 0.0

    e_prev = 0.0
    x_n = 0.0
    theta = 90.0
    T = 1/fs


    time_prev = time.time()
    time_start = time.time()
    printNow = time.time()
    printDelay = 0.1

    while runTimeBool:
        theta_fb = round(encoderFeedback * 0.9, 3)
        Ts_prev = 0

        ####################################
        #Hvor ofte posisjoner skal sendes ut
        ####################################
        if time.time() >= time_prev + 0.001:
            time_prev = time.time()
            i = round((time_prev - time_start) / T)
            if i > len(fpos) - 1:
                theta = fpos[len(fpos) - 1]
            else:
                theta = fpos[i]

        ##########################################
        #Hvor ofte nye x_n verdier skal bli endret
        ##########################################
        if time.time() >= Ts_prev + 0.00025:
            Ts_prev = time.time()
            e = errorCorrection(theta, theta_fb)

            x_n = (A * e) + (B * e_prev) + (C * INT_prev)
            if theta + 0.5 >= theta_fb >= theta - 0.5:
                x_n = 0
                INT_prev = 0

            INT_prev += (0.5 * (e + e_prev) * Ts)
            e_prev = e

            dir(theta, theta_fb)

        if x_n > 100:
            x_n = 100

        if clockwise:
            CW_pwm.ChangeDutyCycle(x_n)
            CCW_pwm.ChangeDutyCycle(0)
        else:
            CW_pwm.ChangeDutyCycle(0)
            CCW_pwm.ChangeDutyCycle(x_n)

        ###############################################
        #Print of different values to analyze and debug
        if time.time() >= printNow + printDelay:
            printNow = time.time()
            print("Theta: ", round(theta, 2), "Theta_fb: ", round(theta_fb, 2), "e: ", round(e, 2), "clockwise: ",
                  clockwise, "x_n: ", round(x_n, 2))

    #############################################
    #Stop the PWM and the Pi after code interrupt
    CW_pwm.ChangeDutyCycle(0)
    CCW_pwm.ChangeDutyCycle(0)
    decoder.cancel()
    pi.stop()
    print("Stopped")


class ComChan(proto_pb2_grpc.streamServicer):
    def SM(self, request, context):
        global runTimeBool
        print("Method called by client")
        PID = threading.Thread(target=controller, args=(request.velocity,
                                                        request.acceleration,
                                                        request.variable1))
        if request.run:
            runTimeBool = request.run
            if request.methodID == 123:
                print("Starting PID")
                PID.start()
        else:
            runTimeBool = request.run

        run = 4
        data = 180
        response = proto_pb2.serverResponse(runTime=run, eData=data)
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