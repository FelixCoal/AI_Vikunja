from fastapi import FastAPI, HTTPException
from schemas import AddTask, Task
from task_service import create_task_from_text

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
    try:
        return create_task_from_text(taskToAdd.text)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc