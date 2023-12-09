from __future__ import print_function

import random
import string
from datetime import datetime

import grpc
import task_db
import task_pb2
import task_pb2_grpc


def generate_random_string(length=5):
    """Generate a random string of given length."""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def generate_random_status():
    """Generate a random task status."""
    return random.choice(list(task_pb2.TaskStatus.values()))

def generate_random_task_id():
    """Generate a random task ID."""
    return random.randint(0, len(task_db.read_db()) + 1)


def run():
    try:
        # Create an insecure gRPC channel
        with grpc.insecure_channel("localhost:8000") as client:
            # Create a gRPC stub
            client_stub = task_pb2_grpc.TaskServiceStub(client)
            
            # Generate random title, description, and status
            random_title = generate_random_string()
            random_description = generate_random_string()
            random_status = generate_random_status()

            # Create a task with random values
            create_task_response = client_stub.CreateTask(
                task_pb2.TaskDetails(
                    taskId=task_pb2.ID(taskId=-1),
                    taskTitle=random_title,
                    description=random_description,
                    status=random_status,
                    dueDate=datetime.now().strftime("%Y-%m-%d")
                )
            )

            print(f"Your Task was created successfully! Your Task ID: {create_task_response.taskId}")
            

            # Get a task by ID
            try:
                get_task_response = client_stub.GetTask(
                    task_pb2.ID(
                        taskId=generate_random_task_id()
                    )
                )
                print(f"Task Details: {get_task_response}")
            except grpc.RpcError as e:
                print(f"{e.details()}")


            # List all tasks
            task_list = client_stub.ListTasks(
                task_pb2.Empty()
            )

            if task_list:
                print("Task List:")
                for task in task_list:
                    print(task)
            else:
                print("No tasks found.")


            # Delete a task by ID
            delete_task = client_stub.DeleteTask(
                task_pb2.ID(
                    taskId=generate_random_task_id()
                )
            )

            print(f"Task with ID {delete_task.taskId} deleted successfully.")


            # Update a task by ID
            update_task = client_stub.UpdateTask(
                task_pb2.TaskDetails(
                    taskId=task_pb2.ID(taskId = generate_random_task_id()),
                    taskTitle=random_title,
                    description=random_description,
                    status=random_status,
                    dueDate=datetime.now().strftime("%Y-%m-%d")
                )
            )

            print(f"Task with ID {update_task.taskId} updated successfully.")
            
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    run()
