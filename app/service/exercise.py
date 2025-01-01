from app.schema.exercise import *
from app.db.connection import *
from uuid import UUID

async def fetch_muscle_groups() -> list[MuscleGroup]:
    async with get_db_connection() as cur:
        await cur.execute(
        '''SELECT 
                name
            FROM 
                muscle_groups''')
        return await cur.fetchall()


async def fetch_exercise_by_id(exercise_id: UUID) -> Exercise:
    async with get_db_connection() as cur:
        await cur.execute(
        '''SELECT 
                e.exercise_id,
                e.name,
                e.description,
                mg.name as muscle_group,
                e.created_at,
                e.updated_at
            FROM 
                exercises e
            JOIN 
                exercise_muscle_groups emg ON e.exercise_id = emg.exercise_id
            JOIN 
                muscle_groups mg ON emg.muscle_group_id = mg.muscle_group_id
            WHERE
                e.exercise_id = %s''', (exercise_id,))
        
        return await cur.fetchone()
    
async def fetch_all_exercises(page: int, limit: int) -> list[Exercise]:
    async with get_db_connection() as cur:
        await cur.execute(
        '''SELECT 
                e.exercise_id,
                e.name,
                e.description,
                mg.name as muscle_group,
                e.created_at,
                e.updated_at
            FROM 
                exercises e
            JOIN 
                exercise_muscle_groups emg ON e.exercise_id = emg.exercise_id
            JOIN 
                muscle_groups mg ON emg.muscle_group_id = mg.muscle_group_id
            LIMIT %s OFFSET %s''', (limit, (page - 1) * limit))
        return await cur.fetchall()
    
async def fetch_exercises_by_muscle_group(muscle_group: str, page: int, limit: int) -> list[Exercise]:
    async with get_db_connection() as cur:
        await cur.execute(
        '''SELECT 
                e.exercise_id,
                e.name,
                e.description,
                mg.name as muscle_group,
                e.created_at,
                e.updated_at
            FROM 
                exercises e
            JOIN 
                exercise_muscle_groups emg ON e.exercise_id = emg.exercise_id
            JOIN 
                muscle_groups mg ON emg.muscle_group_id = mg.muscle_group_id
            WHERE
                mg.name = %s
            LIMIT %s OFFSET %s''', (muscle_group, limit, (page - 1) * limit))
        return await cur.fetchall()