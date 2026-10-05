import sys
import os
import traceback
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

try:
    backend_path = os.path.join(os.path.dirname(__file__), '..', 'Backend')
    sys.path.insert(0, backend_path)
    from main import app as backend_app
    app.mount("/api", backend_app)
except Exception as e:
    err = traceback.format_exc()
    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def catch_all(path_name: str):
        return JSONResponse(status_code=500, content={"error": "Backend failed to load", "details": err})

