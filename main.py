import os
import psycopg2
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Connect once (simple for demo)
conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
cur = conn.cursor()

app = FastAPI()

# Store active clients
clients = []


@app.websocket("/ws")
async def chat(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            # Open a fresh cursor for every insert
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO messages (id, sender_id, content) VALUES (gen_random_uuid(), NULL, %s)",
                    (data,),
                )
                conn.commit()

            # Broadcast to all clients
            for client in clients:
                await client.send_text(data)

    except WebSocketDisconnect:
        clients.remove(websocket)
