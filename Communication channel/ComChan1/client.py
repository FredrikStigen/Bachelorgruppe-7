import grpc
import proto_pb2
import proto_pb2_grpc

SERVER_ADDRESS = 'localhost:9999'

def exchangeMethod(stub):
    print("Exchange started")
    request = proto_pb2.Request(message=("Hello from client"))
    response = stub.exchange(request)
    print("Response from server: {}".format(response))
    print("Exchange over")

def main():
    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        stub = proto_pb2_grpc.baseServiceStub(channel)
        exchangeMethod(stub)