from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_conn
from models import init_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Initialize DB
init_db()


class User(BaseModel):
    username: str


class Message(BaseModel):
    username: str
    content: str

@app.get("/")
async def read_root():
    return {"message": "Hello, Server is running."}


@app.post("/users/")
def create_user(user: User):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username) VALUES (%s) RETURNING id",
                (user.username,),
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            return {"id": user_id, "username": user.username}
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        conn.close()


@app.post("/messages/")
def send_message(msg: Message):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM users WHERE username = %s", (msg.username,))
        user = cur.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        cur.execute(
            "INSERT INTO messages (user_id, content) VALUES (%s, %s)",
            (user[0], msg.content),
        )
        conn.commit()
    conn.close()
    return {"status": "Message sent"}


@app.get("/messages/")
def get_messages():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("""
        SELECT u.username, m.content, m.created_at
        FROM messages m
        JOIN users u ON m.user_id = u.id
        ORDER BY m.created_at DESC
        LIMIT 20
        """)
        rows = cur.fetchall()
    conn.close()
    return [{"username": r[0], "content": r[1], "created_at": r[2]} for r in rows]
