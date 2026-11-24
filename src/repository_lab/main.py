from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from repository_lab.database import init_db
from repository_lab.items import router as items_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(
    title="Repository Lab API",
    description="Simple REST API created with FastAPI",
    lifespan=lifespan,
)
app.include_router(items_router)


@app.get("/info")
def get_info() -> dict[str, str]:
    return {"service": "Repository Lab API"}


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to Repository Lab API"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "Repository Lab API is running",
    }
