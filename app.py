import uvicorn

from src.apis.routes import app


if __name__ == "__main__":
    uvicorn.run("app:app", port=9000, reload=True)