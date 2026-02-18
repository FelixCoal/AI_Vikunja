from dotenv import load_dotenv
import requests
import os
from schemas import Task

load_dotenv() # Load environment variables from .env file

def get_labels():
    endpoint = "/labels"
    url = f"{os.getenv('VIKUNJA_BASE_URL')}{endpoint}"
    headers = {
        "Authorization": f"Bearer {os.getenv('VIKUNJA_API_KEY')}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching labels: {e}")
        return None


def get_projects():
    endpoint = "/projects"
    url = f"{os.getenv('VIKUNJA_BASE_URL')}{endpoint}"
    headers = {
        "Authorization": f"Bearer {os.getenv('VIKUNJA_API_KEY')}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching projects: {e}")
        return None

def get_tasks():
    endpoint = "/tasks"
    url = f"{os.getenv('VIKUNJA_BASE_URL')}{endpoint}"
    headers = {
        "Authorization": f"Bearer {os.getenv('VIKUNJA_API_KEY')}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching tasks: {e}")
        return None

def add_task(task: Task):
    endpoint = "/projects/{project_id}/tasks".format(project_id=task.project_id)
    url = f"{os.getenv('VIKUNJA_BASE_URL')}{endpoint}"
    headers = {
        "Authorization": f"Bearer {os.getenv('VIKUNJA_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "title": task.title,
        "description": task.description,
    }
    
    try:
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        print(f"Error adding task: {e}")
        return None

def complete_task(task_id):
    return None