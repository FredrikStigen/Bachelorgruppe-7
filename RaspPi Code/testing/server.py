import grpc
import proto_pb2
import proto_pb2_grpc
from concurrent import futures
#import Motion_Profile_AtoB_Test
#import PWM
import PID
import multiprocessing

SERVER_ADDRESS = 'localhost:9999'


def serverRun(run=True):
    #PWM.running(run)
    PID.PID_Controller(run)

def serverStop(run=False):
    PID.PID_Controller(False)

t2 = multiprocessing.Process(target=serverRun)
t3 = multiprocessing.Process(target=serverStop)

class ComChan(proto_pb2_grpc.streamServicer):
    def SM(self, request, context):
        print("Call from client...")

        if request.run:
            t2.start()
        else:
            t3.start()



        run = 1
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
    t1 = multiprocessing.Process(target=main())
    t1.start()