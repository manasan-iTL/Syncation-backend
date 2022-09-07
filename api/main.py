from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import task, done, websocket
import socketio


app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://7fc7-2400-2412-480-6400-8ec-59-912b-22b5.jp.ngrok.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

socket_app = socketio.ASGIApp(websocket.sio)

app.include_router(task.router)
app.include_router(done.router)

@app.get("/hello")
async def hello():
    return {"message": "hello world!"}

app.mount("/ws", socket_app) 