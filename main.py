from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.websockets import WebSocket # Added for WebSocket endpoint
import json # Added for message parsing

app = FastAPI()

# TODO: Initialize Postgres database connection here

# TODO: Initialize Ollama and Qwen3 LLM service clients here


@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # TODO: Integrate with LLM service for chat responses
    # TODO: Store chat history in Postgres database
    try:
        while True:
            data = await websocket.receive_text()
            # For now, just echo the message back
            # Replace with LLM interaction and DB storage
            await websocket.send_text(f"Message text was: {data}")
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
