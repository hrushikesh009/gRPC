import os

from grpc_tools import protoc

current_directory = os.getcwd()

proto_file_path = os.path.join(current_directory, "task.proto")
output_directory = current_directory

protoc.main(
    (
        "",
        f"-I{current_directory}",
        f"--python_out={output_directory}",
        f"--grpc_python_out={output_directory}",
        proto_file_path,
    )
)
