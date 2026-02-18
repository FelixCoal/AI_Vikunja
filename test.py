from main import add_task
from schemas import AddTask, Task
import os

def test_add_task():
    # Create a sample AddTask input
    add_task_input = AddTask(text="Finish the Philosophy report by next week")

    # Call the add_task function
    new_task = add_task(add_task_input)

    # Check if the new task has the expected structure
    assert isinstance(new_task, Task)
    assert new_task.title is not None
    assert new_task.description is not None
    assert new_task.project_id is not None

test_add_task()