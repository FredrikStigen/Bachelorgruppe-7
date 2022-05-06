import grpc
import proto_pb2
import proto_pb2_grpc
from concurrent import futures
#import Motion_Profile_AtoB_Test
import PID
import threading
import multiprocessing

SERVER_ADDRESS = 'localhost:9999'

def thread_func(vel, acc, pos):
    PID.PID_Controller(vel, acc, pos)

class ComChan(proto_pb2_grpc.streamServicer):
    def SM(self, request, context):
        print("Connection attempt from client:")
        #t2 = threading.Thread(target=thread_func, args=(request.velocity, request.acceleration, request.variable1))
        t2 = multiprocessing.Process(target=thread_func, args=(request.velocity, request.acceleration, request.variable1))
        if request.run:
            if request.methodID == 123:
                #t2 = threading.Thread(target=thread_func(request.velocity, request.acceleration, request.variable1))
                #t2 = threading.Thread(target=thread_func, args=(request.velocity, request.acceleration, request.variable1))
                t2.start()
        else:
            if t2.is_alive():
                t2.terminate()
                print("Process stopped")
            else:
                print("No process alive")



        run = 4
        data = 180
        response = proto_pb2.serverResponse(runTime=run, eData=data)
        return response

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    proto_pb2_grpc.add_streamServicer_to_server(ComChan(), server)
    server.add_insecure_port(SERVER_ADDRESS)

    print("Server is running...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    t1 = threading.Thread(target=main())
    t1.start()