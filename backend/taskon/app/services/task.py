from sqlalchemy.orm import Session

from app.dtos.taskdto import TaskDto, TaskCreateDto, TaskUpdateDto
from app.repositories.task import TaskRepository

class TaskNotFoundException(Exception):
    """Task not found in the DB"""

class TaskService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.task_repo = TaskRepository(db)

    def get_all(self) -> list[TaskDto]:
        tasks = self.task_repo.get_all()
        return [TaskDto.model_validate(task) for task in tasks]

    def get_by_id(self, task_id: str) -> TaskDto:
        task = self.task_repo.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundException("Task not found")
        return TaskDto.model_validate(task)

    def create(self, task_create: TaskCreateDto) -> TaskDto:
        new_task = self.task_repo.create(task_create.title)
        self.db.commit()

        return TaskDto.model_validate(new_task)

    def update(self, task_id: str, task_update: TaskUpdateDto) -> TaskDto:
        updating_task = self.task_repo.get_by_id(task_id)
        if updating_task is None:
            raise TaskNotFoundException("Task not found")

        if task_update.title is not None:
            updating_task.title = task_update.title
        if task_update.completed is not None:
            updating_task.completed = task_update.completed

        self.db.commit()

        return TaskDto.model_validate(updating_task)

    def delete(self, task_id: str) -> None:
        deleting_task = self.task_repo.get_by_id(task_id)
        if deleting_task is None:
            raise TaskNotFoundException("Task not found")

        self.task_repo.delete(deleting_task)
        self.db.commit()
