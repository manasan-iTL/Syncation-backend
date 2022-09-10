from fastapi import FastAPI
from api.routers import room, user, task, done

app = FastAPI()
app.include_router(room.router)
app.include_router(user.router)
app.include_router(task.router)
app.include_router(done.router)

# @app.get("/hello")
# async def hello():
#     return {"message": "hello world!"}