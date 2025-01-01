import datetime
from uuid import UUID
from pydantic import BaseModel

class Exercise(BaseModel):
    exercise_id: UUID
    name: str
    muscle_group: str
    description: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime

class MuscleGroup(BaseModel):
    name: str