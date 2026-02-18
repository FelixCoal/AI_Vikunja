from fastapi import FastAPI
from schemas import AddTask, Task
from vikunja import get_projects, get_tasks, add_task as create_vikunja_task
from prompt import MAIN_PROMPT
from llm import ask_together
import json

app = FastAPI()

@app.get("/add_task")
def add_task(taskToAdd: AddTask):
    print("Received task to add:", taskToAdd.text)
    projects = get_projects()
    tasks = get_tasks()
    print("Fetched projects")
    print("Fetched tasks")

    input = MAIN_PROMPT.format(projects=projects, tasks=tasks, user_input=taskToAdd.text)
    response = ask_together(input)
    response = json.loads(response)

    new_task = Task(
        title=response["title"],
        description=response["description"],
        project_id=response["project_id"],
    )

    print("Adding new task to Vikunja:", new_task)
    create_vikunja_task(new_task)

    return new_task