# backend/app/main.py
from fastapi import FastAPI
# from fastapi.responses import FileResponse # FileResponse will not be used by backend directly
from pathlib import Path
from fastapi.websockets import WebSocket # Will be moved to an endpoint file
import json # For WebSocket, to be moved

# Import API router and settings
from .api.v1.api import api_router
from .core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# TODO: Initialize Postgres database connection here (e.g. using db.session.init_db(settings.SQLALCHEMY_DATABASE_URI))
# TODO: Initialize Ollama and Qwen3 LLM service clients here (e.g. llm.clients.ollama_client.init_client(settings.OLLAMA_API_BASE))


# Include the API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# The old root endpoint serving index.html is removed.
# Frontend Nginx will handle serving static files.

# The old WebSocket endpoint - to be moved to app/api/v1/endpoints/websocket.py or similar
# For now, it's commented out here to avoid conflicts and keep track.
# @app.websocket("/ws_example_old_location") # Renamed to avoid conflict if an actual /ws is added to router
# async def websocket_endpoint_old(websocket: WebSocket):
#     await websocket.accept()
#     # TODO: Integrate with LLM service for chat responses
#     # TODO: Store chat history in Postgres database
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await websocket.send_text(f"Message text was: {data} (from old location)")
#     except Exception as e:
#         print(f"WebSocket Error: {e}")
#     finally:
#         await websocket.close()

# A simple health check endpoint at the root of the app for basic app status (optional)
@app.get("/health", tags=["Application Health"])
async def app_health_check():
    return {"status": "application healthy"}

# Gunicorn runs this app:app instance, so no if __name__ == "__main__": block.
# Example: CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "app.main:app"]
# Note the module path for Gunicorn will be app.main:app assuming WORKDIR in Dockerfile is /app (which is backend/app)
# Or if WORKDIR is / (project root), then backend.app.main:app
# The current backend/Dockerfile has WORKDIR /app, which means it refers to backend/
# So the command should be `gunicorn ... app.main:app` if main.py is in backend/app/
# Or `main:app` if main.py is in backend/ (the WORKDIR).
# The backend Dockerfile is `WORKDIR /app` and then `COPY . .`, meaning /app is the backend directory.
# So, the command `CMD ["gunicorn", ..., "main:app"]` in backend/Dockerfile implies `backend/main.py`.
# This needs to be changed to `app.main:app` in backend/Dockerfile. I'll handle this in a later step if needed.
# For now, this file is backend/app/main.py.
# The existing backend/Dockerfile has `CMD ["gunicorn", ..., "main:app"]`.
# This will need to be updated to `CMD ["gunicorn", ..., "app.main:app"]` because the main.py is now in backend/app/
# I will make a note to update the Dockerfile later.

# For now, let's add the health check that was in the instructions:
# This is a bit redundant with the /health above, but following instructions.
# The instruction one was /api/v1/health, this one is /api/v1/health
# The one in instruction was to be created in `backend/app/main.py`
# The file `backend/app/api/v1/endpoints/health.py` will have `/ping`
# The `app.include_router(api_router, prefix=settings.API_V1_STR)` will make it available.
# So, I will remove the @app.get("/api/v1/health") from here if it's meant to be from the router.

# The instructions for Step 5's app/main.py had:
# @app.get("/api/v1/health")
# async def health_check():
# return {"status": "healthy"}
# This is fine as a direct endpoint on app, or it can come from a router.
# Let's assume it's a direct one for now, distinct from the router's /ping
@app.get(settings.API_V1_STR + "/health", tags=["Direct Health Check"])
async def direct_health_check():
    return {"status": "healthy from app.main direct"}

# The websocket from old main.py needs to be moved.
# I will create a new endpoint file for it as part of this restructuring.
# backend/app/api/v1/endpoints/chat.py could be a place.
# For now, the definition is lost from old main.py unless I put it here.
# I will put the websocket code into a new file `backend/app/api/v1/endpoints/websocket_echo.py`

# The lines for api_router and settings are not commented out as per step 10 preview.
# title and openapi_url are also set.
# The websocket code from old main.py is not here, it will be moved to a dedicated endpoint file.
# The FileResponse for index.html is correctly removed.
# The if __name__ block is correctly removed.
# The placeholder /api/v1/health endpoint is added.
# The main structure looks fine according to the plan.
