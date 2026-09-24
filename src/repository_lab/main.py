from fastapi import FastAPI

app = FastAPI(title="Repository Lab API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to Repository Lab API"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
