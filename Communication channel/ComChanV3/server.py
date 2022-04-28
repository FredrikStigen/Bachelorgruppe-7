import grpc
import proto_pb2
import proto_pb2_grpc
import time
from concurrent import futures
import sys

SERVER_ADDRESS = 'localhost:9999'

class ComChan(proto_pb2_grpc.streamServicer):
    def SM(self, request, context):
        print("Connection attempt from client:")
        print(request.methodID)
        print(request.velocity)
        print(request.acceleration)
        print(request.variable1)
        print(request.variable2)

        response = proto_pb2.serverResponse(resp="Methode received, use the following counter to start: ",
                                            startCount=1)
        return response

    def SSM(self, request_iterator, context):
        for response in request_iterator:
            print(response.counter)





def main():
    server = grpc.server(futures.ThreadPoolExecutor())
    proto_pb2_grpc.add_streamServicer_to_server(ComChan(), server)
    server.add_insecure_port(SERVER_ADDRESS)

    print("Server is running...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    main()