import uvicorn
import os
from apis.routes import app


if __name__ == "__main__":
    host: str = os.getenv('API_HOST','127.0.0.1')
    port: int = os.getenv('API_PORT', 9000)

    uvicorn.run("app:app", host=host, port=int(port), reload=True)