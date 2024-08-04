# rpc_protocol.py

import grpc
from concurrent import futures
from proto import agent_pb2, agent_pb2_grpc

class AgentService(agent_pb2_grpc.AgentServiceServicer):
    def ExecuteTask(self, request, context):
        try:
            # Implement task execution logic
            response = agent_pb2.TaskResponse(status="Task executed")
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return agent_pb2.TaskResponse(status="Task failed")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    agent_pb2_grpc.add_AgentServiceServicer_to_server(AgentService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
