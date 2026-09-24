from fastapi import FastAPI

app = FastAPI(
    title="Repository Lab API",
    description="Simple REST API created with FastAPI"
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to Repository Lab API"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
