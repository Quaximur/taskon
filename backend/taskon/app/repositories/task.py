from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.models.task import Task


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[Task]:
        return list(self.db.scalars(select(Task)).all())

    def get_by_id(self, task_id: str) -> Task | None:
        return self.db.get(Task, task_id)

    def create(self, title: str) -> Task:
        new_task = Task(title=title)
        self.db.add(new_task)

        return new_task

    def delete_by_id(self, task_id) -> None:
        self.db.execute(delete(Task).where(Task.id == task_id))

    def delete(self, task: Task) -> None:
        self.db.delete(task)