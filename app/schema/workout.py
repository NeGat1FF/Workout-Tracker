from pydantic import BaseModel, FutureDate
from uuid import UUID
import datetime
from app.schema.exercise import Exercise


class AddExercise(BaseModel):
    exercise_id: UUID
    sets: int
    reps: int
    weight: float
    rest_period: int

class WorkoutCreate(BaseModel):
    title: str
    description: str = ""
    exercises: list[AddExercise] | None = None

class OutExercise(BaseModel):
    workout_exercise_id: UUID
    name: str
    description: str | None
    sets: int
    reps: int
    weight: float
    rest_period: int

class Workout(BaseModel):
    workout_id: UUID
    user_id: UUID
    title: str
    description: str | None
    exercises: list[OutExercise]
    created_at: datetime.datetime
    updated_at: datetime.datetime

class ScheduledWorkout(BaseModel):
    schedule_id: UUID | None = None
    workout_id: UUID
    scheduled_date: FutureDate
    scheduled_time: datetime.time

class WorkoutReport(BaseModel):
    report_id: UUID | None = None
    workout_id: UUID
    note: str
    created_at: datetime.datetime