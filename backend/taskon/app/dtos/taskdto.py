from pydantic import BaseModel, ConfigDict


class TaskDto(BaseModel):
    id: str
    title: str
    completed: bool

    model_config = ConfigDict(from_attributes=True)


class TaskCreateDto(BaseModel):
    title: str


class TaskUpdateDto(BaseModel):
    title: str | None = None
    completed: bool | None = None
