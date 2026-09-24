Repository Lab API

A small FastAPI application with root and health-check endpoints.

## Installation

Create and activate a virtual environment, then install the project dependencies:

```powershell
uv sync
.\.venv\Scripts\Activate.ps1
```

## Run the application

Start the development server from the project root:

```powershell
uv run uvicorn repository_lab.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Endpoints

### `GET /`

Returns a welcome message:

```json
{"message": "Welcome to Repository Lab API"}
```

### `GET /health`

Returns the application health status:

```json
{"status": "ok"}
```
