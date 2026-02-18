# AI Vikunja Task Assistant

AI Vikunja Task Assistant is a small FastAPI service that converts free-form task text into a structured Vikunja task using an LLM (Together AI), then creates that task in Vikunja via its API.

## How it works

1. You call the `/add_task` endpoint with free text.
2. The service fetches existing projects and tasks from Vikunja.
3. It sends context + user input to Together AI.
4. The model returns JSON with `title`, `description`, and `project_id`.
5. The service creates the task in Vikunja.

## Tech stack

- Python 3.11
- FastAPI
- Uvicorn
- Requests
- Together AI SDK
- python-dotenv

## Project structure

- `main.py` — FastAPI app and `/add_task` endpoint
- `vikunja.py` — Vikunja API helpers (projects, tasks, create task)
- `llm.py` — Together AI client + completion call
- `prompt.py` — Prompt template with context injection
- `schemas.py` — Pydantic request/response models
- `test.py` — very basic smoke-style test call
- `Dockerfile` — container image definition

## Requirements

- Python 3.11+
- A Vikunja instance and API token
- A Together AI API key

## Environment variables

Create a `.env` file in the project root:

```env
TOGETHER_API_KEY=your_together_api_key
VIKUNJA_BASE_URL=https://your-vikunja-domain/api/v1
VIKUNJA_API_KEY=your_vikunja_api_token
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run locally

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open docs at:

- http://localhost:8000/docs

## Run as MCP server

This project also includes an MCP server that exposes exactly one tool:

- `add_task` (same behavior as `POST /add_task`)

Start it over stdio:

```bash
python mcp_server.py
```

It reuses the same environment variables from `.env` (`TOGETHER_API_KEY`,
`VIKUNJA_BASE_URL`, `VIKUNJA_API_KEY`).

## API usage

### Add task

Endpoint currently defined as:

- `POST /add_task`

Example request:

```bash
curl -X POST "http://localhost:8000/add_task" \
  -H "Content-Type: application/json" \
  -d '{"text":"Finish the philosophy report by next week"}'
```

Example response:

```json
{
  "title": "Finish philosophy report",
  "description": "Write and finalize the philosophy report by next week.",
  "project_id": 3
}
```

## Run with Docker

Build image:

```bash
docker build -t ai-vikunja .
```

Run container:

```bash
docker run --rm -p 8000:8000 \
  -e TOGETHER_API_KEY="your_together_api_key" \
  -e VIKUNJA_BASE_URL="https://your-vikunja-domain/api/v1" \
  -e VIKUNJA_API_KEY="your_vikunja_api_token" \
  ai-vikunja
```

## Run API + MCP together (Docker Compose)

Start both services:

```bash
docker compose up --build
```

- `api` service runs FastAPI on `http://localhost:8000`
- `mcp` service runs `python mcp_server.py`

Run only one service if needed:

```bash
docker compose up --build api
docker compose up --build mcp
```

## Notes

- The model prompt requests strict JSON output; malformed model output may cause parsing errors.
- If Vikunja or Together credentials are missing/invalid, requests will fail.
- `test.py` calls the live flow and is not a mocked unit test.

## Future improvements

- Add proper unit tests with mocked LLM and Vikunja API calls
- Add validation and fallback handling for non-JSON model responses
