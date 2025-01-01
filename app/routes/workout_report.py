from app.service.user import authenticate_user
from app.service.workout import *
from app.service.workout_report import *
from app.schema.workout import *
from fastapi import APIRouter, Depends

report_router = APIRouter(tags=["report"], prefix="/api/v1")

@report_router.post("/report", status_code=200, summary="Create a workout report")
async def create_report(report: WorkoutReport, claims: dict = Depends(authenticate_user)):
    if await is_user_authorised_for_workout(report.workout_id, claims['uid']):
        return await create_workout_report(report, claims['uid'])
    
@report_router.get("/report/{workout_id}", status_code=200, summary="Get all reports for a workout")
async def get_reports_for_workout(workout_id: UUID, claims: dict = Depends(authenticate_user)) -> list[WorkoutReport]:
    if await is_user_authorised_for_workout(workout_id, claims['uid']):
        return await get_workout_reports(workout_id)
    
@report_router.get("/report/{report_id}", status_code=200, summary="Get a workout report")
async def get_report(report_id: UUID, claims: dict = Depends(authenticate_user)) -> WorkoutReport:
    if await is_user_authorised_for_report(report_id, claims['uid']):
        return await get_workout_report(report_id)
    
@report_router.get("/report", status_code=200, summary="Get all reports for a user")
async def get_user_reports(claims: dict = Depends(authenticate_user)) -> list[WorkoutReport]:
    return await get_user_reports(claims['uid'])

@report_router.put("/report/{report_id}", status_code=200, summary="Update a workout report")
async def update_report(report_id: UUID, note: str, claims: dict = Depends(authenticate_user)) -> WorkoutReport:
    if await is_user_authorised_for_report(report_id, claims['uid']):
        return await update_workout_report(report_id, note)
    
@report_router.delete("/report/{report_id}", status_code=204, summary="Delete a workout report")
async def delete_report(report_id: UUID, claims: dict = Depends(authenticate_user)):
    if await is_user_authorised_for_report(report_id, claims['uid']):
        return await delete_workout_report(report_id)
