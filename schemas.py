from pydantic import BaseModel, Field, ConfigDict

class AddTask(BaseModel):
    text: str = Field(
        ...,
        description=(
            "Raw user intent in natural language. The API uses this text, together "
            "with Vikunja project/task context, to generate a structured task."
        ),
        examples=[
            "Finish the philosophy report by next week and share a draft on Monday"
        ],
        min_length=3,
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "text": "Schedule dentist appointment next Thursday afternoon"
                }
            ]
        }
    )

class Task(BaseModel):
    title: str = Field(
        ...,
        description="Short actionable task title generated from user intent.",
        examples=["Finish philosophy report"],
        min_length=1,
    )
    description: str = Field(
        ...,
        description=(
            "Expanded task details. Can include assumptions inferred from user text."
        ),
        examples=["Write and finalize the philosophy report by next week."],
    )
    project_id: int = Field(
        ...,
        description="Numeric Vikunja project ID where the task should be created.",
        examples=[3],
        ge=1,
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Prepare weekly team sync notes",
                    "description": "Collect updates from each workstream and publish agenda by Friday.",
                    "project_id": 2,
                }
            ]
        }
    )