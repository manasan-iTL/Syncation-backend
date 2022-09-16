from fastapi import FastAPI
from api.routers import room, task, done, websocket
from fastapi.middleware.cors import CORSMiddleware
import socketio

app = FastAPI()
app.include_router(room.router)
app.include_router(task.router)
app.include_router(done.router)


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

app.mount("/ws", socket_app)
