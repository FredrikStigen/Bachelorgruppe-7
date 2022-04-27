import grpc
import func_pb2
import func_pb2_grpc

SERVER_ADDRESS = 'localhost:9999'
PIADDRESS = '169.254.165.33:9999'

def S_S_M(stub):
    print("Calling method from client")
    request = func_pb2.Request(methodID=2,
                               runTime=3,
                               velocity=120,
                               acceleration=6,
                               variable1=30,
                               variable2=90)
    response_iterator = stub.SSM(request)
    for response in response_iterator:
        print("Connection Verification: {}".format(response.connVer))
        print("System position: {}".format(response.encoderData))

def main():
    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        stub = func_pb2_grpc.ComChanStub(channel)
        S_S_M(stub)


if __name__ == '__main__':
    main()