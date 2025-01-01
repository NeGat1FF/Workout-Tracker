from app.service.user import authenticate_user
from app.service.workout import *
from app.service.schedule_workout import *
from app.schema.workout import *
from fastapi import APIRouter, Depends

schedule_router = APIRouter(tags=["schedule"], prefix="/api/v1")

@schedule_router.post("/schedule", status_code=200, summary="Schedule a workout")
async def schedule_workout_for_user(schedule: ScheduledWorkout, claims: dict = Depends(authenticate_user)):
    if await is_user_authorised_for_workout(schedule.workout_id, claims['uid']):
        return await schedule_workout(schedule, claims['uid'])
    
@schedule_router.get("/schedule", status_code=200, summary="Get all scheduled workouts")
async def get_scheduled_workouts_for_user(claims: dict = Depends(authenticate_user)) -> list[ScheduledWorkout]:
    return await get_scheduled_workouts(claims['uid'])

@schedule_router.get("/schedule/{workout_id}", status_code=200, summary="Get scheduled workouts for a workout")
async def get_schedule_for_workout(workout_id: UUID, claims: dict = Depends(authenticate_user)) -> list[ScheduledWorkout]:
    if await is_user_authorised_for_workout(workout_id, claims['uid']):
        return await get_schedules_for_workout(workout_id)
    
@schedule_router.delete("/schedule/{schedule_id}", status_code=204, summary="Delete a scheduled workout")
async def delete_scheduled_workout(schedule_id: UUID, claims: dict = Depends(authenticate_user)):
    if await is_user_authorised_for_schedule(schedule_id, claims['uid']):
        return await delete_scheduled_workout(schedule_id)