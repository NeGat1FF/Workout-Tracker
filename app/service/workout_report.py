from app.schema.workout import *
from app.db.connection import *
from fastapi import HTTPException
from uuid import UUID

async def is_user_authorised_for_report(report_id: UUID, user_id: UUID) -> bool:
    async with get_db_connection() as cur:
        await cur.execute(
        '''SELECT 
            user_id
        FROM 
            workout_reports
        WHERE
            report_id = %s;''', (report_id,))
        report_user = await cur.fetchone()

    if report_user == None:
        raise HTTPException(status_code=404, detail="Report not found")
    
    if str(report_user['user_id']) != user_id:
        raise HTTPException(status_code=403, detail="User not authorised")
    
    return True

async def create_workout_report(report: WorkoutReport, user_id: UUID) -> WorkoutReport:
    async with get_db_connection() as cur:
        await cur.execute(
        '''INSERT INTO 
                workout_reports (workout_id, note) 
            VALUES 
                (%s, %s)
            RETURNING report_id, workout_id, note, created_at''', (report.workout_id, report.note))
        return WorkoutReport.model_validate(await cur.fetchone())
    
async def get_workout_reports(workout_id: UUID) -> list[WorkoutReport]:
    async with get_db_connection() as cur:
        await cur.execute(
        '''SELECT 
            report_id,
            workout_id,
            note,
            created_at
        FROM 
            workout_reports
        WHERE
            workout_id = %s;''', (workout_id,))
        return await cur.fetchall()
    
async def get_workout_report(report_id: UUID) -> WorkoutReport:
    async with get_db_connection() as cur:
        await cur.execute(
        '''SELECT 
            report_id,
            workout_id,
            note,
            created_at
        FROM 
            workout_reports
        WHERE
            report_id = %s;''', (report_id,))
        return await cur.fetchone()
    
async def get_user_reports(user_id: UUID) -> list[WorkoutReport]:
    async with get_db_connection() as cur:
        await cur.execute(
        '''SELECT 
            report_id,
            workout_id,
            note,
            created_at
        FROM 
            workout_reports
        WHERE
            user_id = %s;''', (user_id,))
        return await cur.fetchall()
    
async def update_workout_report(report_id: UUID, note: str) -> WorkoutReport:
    async with get_db_connection() as cur:
        await cur.execute(
        '''UPDATE 
                workout_reports 
            SET 
                note = %s
            WHERE 
                report_id = %s
            RETURNING report_id, workout_id, note, created_at''', (note, report_id))
        return WorkoutReport.model_validate(await cur.fetchone())
    

async def delete_workout_report(report_id: UUID) -> None:
    async with get_db_connection() as cur:
        await cur.execute(
        '''DELETE FROM 
                workout_reports 
            WHERE 
                report_id = %s''', (report_id,))
        return None
