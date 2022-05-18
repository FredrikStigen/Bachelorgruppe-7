import grpc
import proto_pb2
import proto_pb2_grpc
from concurrent import futures

SERVER_ADDRESS = 'localhost:9999'

class testServer(proto_pb2_grpc.baseServiceServicer):
    def exchange(self, request, context):
        print("From client: {}".format(request.message))
        response = proto_pb2.Response(message=("Hello from server"))
        return response

def main():
    print("Server started")
    server = grpc.server(futures.ThreadPoolExecutor())
    proto_pb2_grpc.add_baseServiceServicer_to_server(testServer(), server)
    server.add_insecure_port(SERVER_ADDRESS)
    server.start()
    server.wait_for_termination()

