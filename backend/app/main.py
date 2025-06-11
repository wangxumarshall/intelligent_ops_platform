# backend/app/main.py
from fastapi import FastAPI
# from fastapi.responses import FileResponse # FileResponse will not be used by backend directly

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

# For now, let's add the health check that was in the instructions:
# This is a bit redundant with the /health above, but an explicit requirement.
# The file `backend/app/api/v1/endpoints/health.py` will have `/ping`.
# The `app.include_router(api_router, prefix=settings.API_V1_STR)` will make it available under `/api/v1/health/ping`.

# The instructions for Step 5 of the backend refactor subtask for app/main.py had:
# @app.get("/api/v1/health")
# async def health_check():
# return {"status": "healthy"}
# This specific endpoint is still present.
@app.get(settings.API_V1_STR + "/health", tags=["Direct Health Check"])
async def direct_health_check():
    return {"status": "healthy from app.main direct"}

# Obsolete WebSocket code and related comments have been removed.
# FileResponse import is not needed.
# Path, WebSocket, json imports were removed.
# Gunicorn command comment block was removed.
