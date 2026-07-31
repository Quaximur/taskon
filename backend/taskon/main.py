from contextlib import asynccontextmanager
from typing import Type
from uuid import uuid4
from fastapi import Depends, FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, Session
from sqlalchemy.testing.schema import mapped_column

DATABASE_URL = "postgresql+psycopg://taskon_admin:adm@127.0.0.1:15432/taskon_db"
engine = create_engine(DATABASE_URL)
session_local = sessionmaker(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


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


def task_orm_to_dto(task: Task) -> TaskDto:
    return TaskDto(id=task.id, title=task.title, completed=task.completed)


@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db)) -> list[TaskDto]:
    existing_tasks = db.scalars(select(Task)).all()
    return [task_orm_to_dto(task) for task in existing_tasks]


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateDto, db: Session = Depends(get_db)) -> TaskDto:
    new_task = Task(title=payload.title)
    db.add(new_task)
    db.commit()

    return task_orm_to_dto(new_task)


@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateDto, db: Session = Depends(get_db)) -> TaskDto:
    updating_task: Task | None  = db.get(Task, task_id)
    if updating_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if payload.title is not None:
        updating_task.title = payload.title
    if payload.completed is not None:
        updating_task.completed = payload.completed

    db.commit()

    return task_orm_to_dto(updating_task)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)) -> None:
    deleted_count = db.execute(delete(Task).where(Task.id == task_id))
    if deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db.commit()
    return None
