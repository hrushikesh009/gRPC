# TaskManager Project

TaskManager is a simple project for managing tasks using gRPC and JSON storage.

## Table of Contents

- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)

## Installation

### Prerequisites

Make sure you have the following tools installed on your system:

- Python (>=3.6)
- gRPC Tools

### Clone the Repository

```bash
git clone https://github.com/your-username/TaskManager.git
cd TaskManager
```
### Install Dependencies
```
pip install -r requirements.txt
```

### Generate gRPC Files
```
python generate_grpc_files.py
```

## Project Structure
TaskManager/

├── task.proto

├── task_pb2.py

├── task_pb2_grpc.py

├── db.json

├── task_manager_server.py

├── task_manager_client.py

├── generate_grpc_files.py

├── README.md

└── requirements.txt

* `task.proto:` Protocol Buffer definition file.
* `task_pb2.py` and `task_pb2_grpc.py`: Generated Python files for gRPC.
* `db.json`: JSON file used as a simple database.
* `task_manager/`: Python package containing server and client scripts.
* `task_db.py`: Helper Function to insert,update and delete JSON Data.
* `generate_grpc_files.py`: Script to generate gRPC files.
* `requirements.txt`: List of project dependencies.
* `README.md`: Project documentation.

## Usuage

### Start the server
```
python task_manager_server.py
```

### Run the Client
```
python task_manager_client.py
```