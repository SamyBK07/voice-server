import json

TASK_FILE = "tasks.json"


def load_tasks():

    try:
        with open(TASK_FILE,"r") as f:
            return json.load(f)
    except:
        return []


def save_tasks(tasks):

    with open(TASK_FILE,"w") as f:
        json.dump(tasks,f,indent=2)


def add_task(title,description):

    tasks = load_tasks()

    task = {
        "id":len(tasks)+1,
        "title":title,
        "description":description,
        "status":"pending"
    }

    tasks.append(task)

    save_tasks(tasks)

    return task
