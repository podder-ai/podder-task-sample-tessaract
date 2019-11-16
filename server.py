"""
DO NOT MODIFY THIS FILE.
"""

import os
import dotenv
from app.task import Task
from podder_task_foundation import MODE, Context
from podder_task_foundation.api import GrpcServer, TaskApiExecutor
from podder_task_foundation.api.protos import pipeline_framework_pb2_grpc

DEFAULT_GRPC_PID_FILE = "/var/run/poc_base.pid"
DEFAULT_PORT = 50051
DEFAULT_MAX_WORKERS = 10

if __name__ == '__main__':
    """
    Run gRPC server.
    """
    task = Task(MODE.PIPELINE)
    dotenv.load_dotenv(".env")
    GrpcServer(
        stdout_file=open(os.getenv("GRPC_LOG"), 'a'),
        stderr_file=open(os.getenv("GRPC_ERROR_LOG"), 'a'),
        pidfile_path=os.getenv("GRPC_PID_FILE", DEFAULT_GRPC_PID_FILE),
        max_workers=os.getenv("GRPC_MAX_WORKERS", DEFAULT_MAX_WORKERS),
        port=os.getenv("GRPC_PORT", DEFAULT_PORT),
        execution_task=Task,
        add_servicer_method=pipeline_framework_pb2_grpc.add_PodderTaskApiServicer_to_server).run()
