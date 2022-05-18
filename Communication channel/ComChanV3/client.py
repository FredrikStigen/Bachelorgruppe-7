import grpc
import proto_pb2
import proto_pb2_grpc
import time


SERVER_ADDRESS = 'localhost:9999'
PIADDRESS = '169.254.165.33:9999'

#Callable client, connection from the GUI
def values(method, run, vel, acc, var=0, var2=0):
    def S_S_M(stub):
        print("Calling method from client")
        request = proto_pb2.clientRequest(methodID=method,
                                          run=run,
                                          velocity=vel,
                                          acceleration=acc,
                                          variable1=var,
                                          variable2=var2)

        response = stub.SM(request)
        print(response)



    with grpc.insecure_channel(PIADDRESS) as channel:
        stub = proto_pb2_grpc.streamStub(channel)
        S_S_M(stub)



'''if __name__ == '__main__':
    values(1, True, 5, 3, 4, 5)'''