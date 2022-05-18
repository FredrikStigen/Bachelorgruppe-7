import time
import datetime
import grpc
import func_pb2
import func_pb2_grpc

import loggingTest


SERVER_ADDRESS = 'localhost:9999'
PIADDRESS = '169.254.165.33:9999'

def values(method, runtime, vel, acc, var=0, var2=0):
    t = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    t = t.replace(":", ".")
    filename = str(("{}.txt".format(t)))
    filepath = "C:/Users/Stigen/Documents/GitHub/Python/Bachelor 2022/CommunicationChannelV2/logs/"

    def S_S_M(stub):
        print("Calling method from client")
        request = func_pb2.Request(methodID=method,
                                   runTime=runtime,
                                   velocity=vel,
                                   acceleration=acc,
                                   variable1=var,
                                   variable2=var2)

        response_iterator = stub.SSM(request)
        timeNow = time.time()
        for response in response_iterator:
            if time.time() - timeNow > 1:
                timeNow = time.time()
                print("1 sec passed")
                loggingTest.x(response.encoderData, filepath, filename)
            print("Session time: {}, expected runtime: {}".format(response.connVer, runtime))
            print("Connection verification: {}".format(response.connVer))
            print("System position: {}".format(response.encoderData))
        print("Methode complete")


    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        stub = func_pb2_grpc.ComChanStub(channel)
        S_S_M(stub)



if __name__ == '__main__':
    values(1, 5, 3, 4, 5, 6)