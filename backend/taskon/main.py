from uuid import uuid4
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)


class TaskScheme(BaseModel):
    id: str
    title: str
    completed: bool


class TaskCreateScheme(BaseModel):
    title: str


tasks: list[TaskScheme] = []


@app.get("/")
def read_tasks():
    return tasks


@app.post("/")
def create_task(payload: TaskCreateScheme) -> TaskScheme:
    new_task = TaskScheme(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(new_task)

    return new_task
