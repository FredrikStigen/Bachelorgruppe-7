from concurrent import futures
import grpc
import func_pb2
import func_pb2_grpc
import time
import sys
SERVER_ADDRESS = 'localhost:9999'

def stop():
    sys.exit()

class CCServer(func_pb2_grpc.ComChanServicer):
    def SSM(self, request, context):
        print("method called externally")
        print(request.methodID)
        print(request.runTime)
        print(request.velocity)
        print(request.acceleration)
        print(request.variable1)
        print(request.variable2)

        def responseGenerator():
            for i in range(int(request.runTime)):
                counter = i
                eData = 445
                response = func_pb2.Response(connVer=counter,
                                             encoderData=eData)
                time.sleep(0.25)
                yield response
        return responseGenerator()


def main():
    server = grpc.server(futures.ThreadPoolExecutor())
    func_pb2_grpc.add_ComChanServicer_to_server(CCServer(), server)
    server.add_insecure_port(SERVER_ADDRESS)

    print("Server is running...")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()