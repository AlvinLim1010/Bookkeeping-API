import uvicorn
import os
from apis.routes import app


if __name__ == "__main__":
    port: int = os.getenv('API_PORT', 9000)

    uvicorn.run("app:app", port=int(port), reload=True)