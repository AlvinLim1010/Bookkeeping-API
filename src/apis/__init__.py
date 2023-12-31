from fastapi import FastAPI
import os


def create_app():
    app = FastAPI(title="Book-Keeping Application",
                description="Book-keeping endpoints using FastAPI",
                version="0.1.0")

    return app