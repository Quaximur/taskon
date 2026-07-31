from contextlib import asynccontextmanager
from uuid import uuid4
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column

DATABASE_URL = "postgresql+psycopg://taskon_admin:adm@127.0.0.1:15432/taskon_db"
engine = create_engine(DATABASE_URL)
session_local = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))


class Task(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)


class TaskDto(BaseModel):
    id: str
    title: str
    completed: bool


class TaskCreateDto(BaseModel):
    title: str


class TaskUpdateDto(BaseModel):
    title: str | None = None
    completed: bool | None = None


tasks: list[TaskDto] = []


@app.get("/tasks")
def read_tasks():
    return tasks


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateDto) -> TaskDto:
    new_task = TaskDto(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(new_task)

    return new_task


@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateDto) -> TaskDto:
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
