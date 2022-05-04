import grpc
import proto_pb2
import proto_pb2_grpc
from concurrent import futures
import Motion_Profile_AtoB_Test


SERVER_ADDRESS = 'localhost:9999'

class ComChan(proto_pb2_grpc.streamServicer):
    def SM(self, request, context):
        print("Connection attempt from client:")
        #print(request.methodID)
        #print(request.velocity)
        #print(request.acceleration)
        #print(request.variable1)
        print(request.variable2)
        if request.methodID == 123:
            Motion_Profile_AtoB_Test.motionProfile(request.velocity,
                                                   request.acceleration,
                                                   request.variable1)


        run = 4
        data = 180
        response = proto_pb2.serverResponse(runTime=run, eData=data)
        return response
def main():
    server = grpc.server(futures.ThreadPoolExecutor())
    proto_pb2_grpc.add_streamServicer_to_server(ComChan(), server)
    server.add_insecure_port(SERVER_ADDRESS)

    print("Server is running...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    main()