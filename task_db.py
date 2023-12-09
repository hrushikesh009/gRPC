import json

from task_pb2 import ID, TaskDetails

DB_FILE = "db.json"

def read_db():
    try:
        with open(DB_FILE, "r") as db:
            data = json.load(db)
        return [create_task_object(item) for item in data]
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []

def create_task_object(item):
    return TaskDetails(
        taskId=ID(taskId=item["id"]),
        taskTitle=item["title"],
        description=item["description"],
        status=item["status"],
        dueDate=item["due-date"]
    )

def write_db(task_dict):
    try:
        with open(DB_FILE, "r") as db:
            data = json.load(db)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = []

    data.append(task_dict)

    with open(DB_FILE, "w") as db:
        json.dump(data, db, indent=2)

def delete_entry(task_id):
    data = read_db()
    data = [row for row in data if row.taskId.taskId != task_id]

    with open(DB_FILE, "w") as db:
        json.dump([task_to_dict(row) for row in data], db, indent=2)

def update_db(task_details):
    data = read_db()
    for row in data:
        if row.taskId.taskId == task_details["id"].taskId:
            row.taskTitle = task_details["title"]
            row.description = task_details["description"]
            row.status = task_details["status"]
            row.dueDate = task_details["due-date"]

    with open(DB_FILE, "w") as db:
        json.dump([task_to_dict(row) for row in data], db, indent=2)

def task_to_dict(task):
    return {
        "id": task.taskId.taskId,
        "title": task.taskTitle,
        "description": task.description,
        "status": task.status,
        "due-date": task.dueDate
    }
