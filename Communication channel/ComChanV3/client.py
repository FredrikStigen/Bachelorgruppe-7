import grpc
import proto_pb2
import proto_pb2_grpc
import time


SERVER_ADDRESS = 'localhost:9999'
PIADDRESS = '169.254.165.33:9999'

def values(method, vel, acc, var=0, var2=0):
    '''t = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    t = t.replace(":", ".")
    filename = str(("{}.txt".format(t)))
    filepath = "C:/Users/Stigen/Documents/GitHub/Python/Bachelor 2022/CommunicationChannelV2/logs/"'''

    def S_S_M(stub):
        print("Calling method from client")
        request = proto_pb2.clientRequest(methodID=method,
                                   velocity=vel,
                                   acceleration=acc,
                                   variable1=var,
                                   variable2=var2)

        response = stub.SM(request)
        print(response)



    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        stub = proto_pb2_grpc.streamStub(channel)
        S_S_M(stub)



if __name__ == '__main__':
    values(1, 5, 3, 4, 5)