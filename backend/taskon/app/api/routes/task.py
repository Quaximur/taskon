from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.api.di import get_task_service
from app.dtos.taskdto import TaskDto, TaskUpdateDto, TaskCreateDto
from app.services.task import TaskService, TaskNotFoundException

router = APIRouter(prefix="/tasks")


@router.get("")
def read_tasks(task_service: TaskService = Depends(get_task_service)) -> list[TaskDto]:
    return task_service.get_all()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateDto, task_service: TaskService = Depends(get_task_service)) -> TaskDto:
    return task_service.create(payload)


@router.patch("/{task_id}")
def update_task(task_id: str, payload: TaskUpdateDto, task_service: TaskService = Depends(get_task_service)) -> TaskDto:
    try:
        return task_service.update(task_id, payload)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, task_service: TaskService = Depends(get_task_service)) -> None:
    try:
        return task_service.delete(task_id)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e)
