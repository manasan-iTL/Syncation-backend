from fastapi import FastAPI
from api.routers import task, done, room

app = FastAPI()
app.include_router(task.router)
app.include_router(done.router)
app.include_router(room.router)
