from fastapi import FastAPI, WebSocket
import json
from initiate import initiate
from edit import edit

app = FastAPI()


@app.websocket("/")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    print("WebSocket connected")
    while True:
        data = await ws.receive_json()
        print(f"Received message: {data}")
        message_type = data.get("type")
        if message_type == "ping":
            await ws.send_json({"type": "pong"})
        elif message_type == "initiate":
            await initiate(ws, data)
        elif message_type == "edit":
            await edit(ws, data)
        else:
            print(f"Unknown message type: {message_type}")
