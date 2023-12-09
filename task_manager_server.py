from concurrent import futures

import grpc
import task_db
import task_pb2
import task_pb2_grpc


class TaskService(task_pb2_grpc.TaskServiceServicer):

    def _read_database(self):
        try:
            return task_db.read_db()
        except Exception as e:
            print(e)

    def CreateTask(self, request, context):
        self.db = self._read_database()

        # Generate a new task ID by finding the maximum existing ID and adding 1
        new_task_id = max([data.taskId.taskId for data in self.db]) + 1 if self.db else 0

        # Create a dictionary with task details
        task_details = {
            "id": new_task_id,
            "title": request.taskTitle,
            "description": request.description,
            "status": request.status,
            "due-date": request.dueDate
        }

        # Write the new task to the database
        task_db.write_db(task_details)

        # Return the new task ID as a response
        return task_pb2.ID(taskId=new_task_id)

    def GetTask(self, request, context):
        self.db = self._read_database()

        # Find the task with the given ID in the database
        for task in self.db:
            if task.taskId == request:
                return task

        # Return a not found response
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Task not found")
        return task_pb2.TaskDetails()


    def DeleteTask(self, request, context):
        # Delete the task with the given ID from the database
        task_db.delete_entry(request.taskId)
        return task_pb2.ID(taskId=request.taskId)

    def ListTasks(self, request, context):
        self.db = self._read_database()
        
        # Yield tasks from the database one by one
        for task in self.db:
            yield task

    def UpdateTask(self, request, context):
        # Create a dictionary with updated task details
        task_details = {
            "id": request.taskId,
            "title": request.taskTitle,
            "description": request.description,
            "status": request.status,
            "due-date": request.dueDate
        }

        # Update the task in the database
        task_db.update_db(task_details)

        # Return the updated task ID as a response
        return task_pb2.ID(taskId=request.taskId.taskId)

def serve():
    # Create a gRPC server with a thread pool executor
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Add the TaskService to the server
    task_pb2_grpc.add_TaskServiceServicer_to_server(TaskService(), server)

    # Specify the server port
    server.add_insecure_port("localhost:8000")

    # Start the server
    print("###### Server is Running ######")
    server.start()

    # Wait for the server to be terminated
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
