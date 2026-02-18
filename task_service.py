import json

from prompt import MAIN_PROMPT
from llm import ask_together
from schemas import Task
from vikunja import get_projects, get_tasks, add_task as create_vikunja_task


def create_task_from_text(text: str) -> Task:
    projects = get_projects()
    tasks = get_tasks()

    if projects is None or tasks is None:
        raise RuntimeError("Failed to fetch projects or tasks from Vikunja")

    prompt = MAIN_PROMPT.format(projects=projects, tasks=tasks, user_input=text)
    response = ask_together(prompt)

    if not response:
        raise RuntimeError("LLM returned an empty response")

    try:
        response_data = json.loads(response)
    except json.JSONDecodeError as exc:
        raise ValueError("Failed to parse model response as JSON") from exc

    new_task = Task(
        title=response_data["title"],
        description=response_data["description"],
        project_id=response_data["project_id"],
    )

    created = create_vikunja_task(new_task)
    if created is None:
        raise RuntimeError("Failed to create task in Vikunja")

    return new_task
