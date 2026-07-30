from uuid import uuid4
from fastapi import FastAPI, status
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


class TaskUpdateScheme(BaseModel):
    title: str | None = None
    completed: bool | None = None


tasks: list[TaskScheme] = []


@app.get("/tasks")
def read_tasks():
    return tasks


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateScheme) -> TaskScheme:
    new_task = TaskScheme(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(new_task)

    return new_task


@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateScheme) -> TaskScheme:
    updating_task = None
    for task in tasks:
        if task.id != task_id:
            continue

        updating_task = task
        if payload.title is not None:
            task.title = payload.title
        if payload.completed is not None:
            task.completed = payload.completed

        break

    return updating_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    for task in tasks:
        if task.id != task_id:
            continue
        tasks.remove(task)
        break
