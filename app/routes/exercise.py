from app.service.exercise import *
from app.schema.exercise import *
from uuid import UUID
from fastapi import APIRouter

exercise_router = APIRouter(tags=["exercise"], prefix="/api/v1")

@exercise_router.get("/exercises",status_code=200, summary="Get all exercises")
async def get_exercises(page: int = 1, limit: int = 10) -> list[Exercise]:
    return await fetch_all_exercises(page, limit)

@exercise_router.get("/exercises/{exercise_id}", status_code=200, summary="Get exercise by ID")
async def get_exercise_by_id(exercise_id: UUID) -> Exercise:
    return await fetch_exercise_by_id(exercise_id)

@exercise_router.get("/muscle_groups", status_code=200, summary="Get all muscle groups")
async def get_muscle_groups() -> list[MuscleGroup]:
    return await fetch_muscle_groups()

@exercise_router.get("/exercises/muscle_group/{muscle_group}", status_code=200, summary="Get exercises by muscle group")
async def get_exercises_by_muscle_group(muscle_group: str, page: int = 1, limit: int = 10) -> list[Exercise]:
    return await fetch_exercises_by_muscle_group(muscle_group, page, limit)