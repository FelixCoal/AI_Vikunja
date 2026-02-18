from pydantic import BaseModel

class AddTask(BaseModel):
    text: str #INncoming free text, to be processed by AI and converted into a task

class Task(BaseModel):
    title: str
    description: str
    project_id: int