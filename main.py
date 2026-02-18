from fastapi import FastAPI, HTTPException
from schemas import AddTask, Task
from vikunja import get_projects, get_tasks, add_task as create_vikunja_task
from prompt import MAIN_PROMPT
from llm import ask_together
import json

app = FastAPI(
    title="AI Vikunja Task Assistant API",
    summary="Transforms natural language into structured Vikunja tasks.",
    description=(
        "This API accepts free-form user task text, enriches it with Vikunja context, "
        "uses an LLM to derive a structured task, and creates that task in Vikunja.\n\n"
        "Agent notes:\n"
        "- Send plain user intent in `text`.\n"
        "- Response contains the normalized task payload that was created.\n"
        "- Failures may come from LLM parsing, missing credentials, or Vikunja API errors."
    ),
    version="1.0.0",
    contact={"name": "AI Vikunja Maintainer"},
)

@app.post(
    "/add_task",
    response_model=Task,
    tags=["Tasks"],
    operation_id="addTaskFromNaturalLanguage",
    summary="Create a Vikunja task from natural language",
    description=(
        "Converts free-form text into a structured Vikunja task and creates it in the "
        "selected project."
    ),
    responses={
        200: {
            "description": "Task was parsed and created successfully in Vikunja.",
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Structured task",
                            "value": {
                                "title": "Finish philosophy report",
                                "description": "Write and finalize the philosophy report by next week.",
                                "project_id": 3,
                            },
                        }
                    }
                }
            },
        },
        500: {
            "description": "Task creation failed due to parsing, credentials, or upstream API issues.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Failed to parse model response as JSON"
                    }
                }
            },
        },
    },
)
def add_task(taskToAdd: AddTask):
    print("Received task to add:", taskToAdd.text)
    projects = get_projects()
    tasks = get_tasks()

    if projects is None or tasks is None:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch projects or tasks from Vikunja",
        )

    print("Fetched projects")
    print("Fetched tasks")

    input = MAIN_PROMPT.format(projects=projects, tasks=tasks, user_input=taskToAdd.text)
    response = ask_together(input)

    if not response:
        raise HTTPException(status_code=500, detail="LLM returned an empty response")

    try:
        response = json.loads(response)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=500, detail="Failed to parse model response as JSON"
        ) from exc

    new_task = Task(
        title=response["title"],
        description=response["description"],
        project_id=response["project_id"],
    )

    print("Adding new task to Vikunja:", new_task)
    created = create_vikunja_task(new_task)
    if created is None:
        raise HTTPException(status_code=500, detail="Failed to create task in Vikunja")

    return new_task