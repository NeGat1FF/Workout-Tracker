from app.service.user import authenticate_user
from app.service.workout import *
from app.schema.workout import *
from fastapi import APIRouter, Depends

workout_router = APIRouter(tags=["workout"], prefix="/api/v1")

@workout_router.post("/workout", status_code=201, summary="Create a new workout")
async def create_workout(workout: WorkoutCreate, claims: dict = Depends(authenticate_user)):
    return await save_workout(workout, claims['uid'])

@workout_router.get("/workout/{workout_id}", status_code=200, summary="Get a workout by ID")
async def get_workout(workout_id: UUID, claims: dict = Depends(authenticate_user)) -> Workout:
    if await is_user_authorised_for_workout(workout_id, claims['uid']) :
        return await get_workout_by_id(workout_id)

@workout_router.put("/workout/{workout_id}", status_code=200, summary="Add an exercise to a workout")
async def add_exercise(workout_id: UUID, exercise: AddExercise, claims: dict = Depends(authenticate_user)):
    if await is_user_authorised_for_workout(workout_id, claims['uid']):
        return await add_exercise_to_workout(workout_id, exercise)
    
@workout_router.delete("/workout/{workout_id}/exercise/{workout_exercise_id}", status_code=204, summary="Delete an exercise from a workout")
async def delete_exercise(workout_id: UUID, workout_exercise_id: UUID, claims: dict = Depends(authenticate_user)):
    if await is_user_authorised_for_workout(workout_id, claims['uid']):
        return await remove_exercise_from_workout(workout_id, workout_exercise_id)
    
@workout_router.delete("/workout/{workout_id}", status_code=204, summary="Delete a workout")
async def delete_workout(workout_id: UUID, claims: dict = Depends(authenticate_user)):
    if await is_user_authorised_for_workout(workout_id, claims['uid']) :
        return await delete_workout_by_id(workout_id)
    
@workout_router.get("/workouts", status_code=200, summary="Get all workouts")
async def get_workouts(claims: dict = Depends(authenticate_user)) -> list[Workout]:
    return await get_workouts_by_user(claims['uid'])

    
