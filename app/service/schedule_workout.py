from app.schema.workout import *
from app.db.connection import *
from fastapi import HTTPException
from uuid import UUID


async def is_user_authorised_for_schedule(schedule_id: UUID, user_id: UUID) -> bool:
    async with get_db_connection() as cur:
        await cur.execute(
        '''SELECT 
            user_id
        FROM 
            scheduled_workouts
        WHERE
            schedule_id = %s;''', (schedule_id,))
        schedule_user = await cur.fetchone()

    if schedule_user == None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    if str(schedule_user['user_id']) != user_id:
        raise HTTPException(status_code=403, detail="User not authorised")
    
    return True

async def schedule_workout(schedule: ScheduledWorkout, user_id: UUID) -> ScheduledWorkout:
    async with get_db_connection() as cur:
        await cur.execute(
        '''INSERT INTO 
                scheduled_workouts (workout_id, user_id, scheduled_date, scheduled_time) 
            VALUES 
                (%s, %s, %s, %s)
            RETURNING *''', (schedule.workout_id, user_id, schedule.scheduled_date, schedule.scheduled_time))
        return ScheduledWorkout.model_validate(await cur.fetchone())
    
async def get_scheduled_workouts(user_id: UUID) -> list[ScheduledWorkout]:
    async with get_db_connection() as cur:
        await cur.execute(
        '''SELECT 
                sw.schedule_id,
                sw.workout_id,
                sw.scheduled_date,
                sw.scheduled_time
            FROM scheduled_workouts sw
            WHERE
                user_id = %s;''', (user_id,))
        return await cur.fetchall()
    
async def get_schedules_for_workout(workout_id: UUID) -> list[ScheduledWorkout]:
    async with get_db_connection() as cur:
        await cur.execute(
        '''SELECT 
            schedule_id,
            workout_id,
            scheduled_date,
            scheduled_time
        FROM 
            scheduled_workouts
        WHERE
            workout_id = %s;''', (workout_id,))
        return await cur.fetchall()
    
async def delete_scheduled_workout(schedule_id: UUID) -> None:
    async with get_db_connection() as cur:
        await cur.execute(
        '''DELETE FROM 
                scheduled_workouts 
            WHERE 
                schedule_id = %s''', (schedule_id,))
        return None
