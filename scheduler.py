import time

from tasks import load_tasks
from planner import generate_tasks


def agent_loop(personality):

    while True:

        tasks = load_tasks()

        if len(tasks) == 0:

            print("No tasks → generating")

            generate_tasks(personality)

        else:

            print("Tasks exist:", len(tasks))

        time.sleep(300)
