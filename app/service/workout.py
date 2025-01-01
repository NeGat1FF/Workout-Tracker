from app.schema.exercise import *
from app.schema.workout import *
from app.db.connection import *
from fastapi import HTTPException
from uuid import UUID

async def is_user_authorised_for_workout(workout_id: UUID, user_id: UUID) -> bool:
    async with get_db_connection() as cur:
        await cur.execute(
        '''SELECT 
            user_id
        FROM 
            workouts
        WHERE
            workout_id = %s;''', (workout_id,))
        workout_user = await cur.fetchone()

    if workout_user == None:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    if str(workout_user['user_id']) != user_id:
        raise HTTPException(status_code=403, detail="User not authorised")
    
    return True
        

async def save_workout(workout: WorkoutCreate, user_id: UUID) -> Workout:
    async with get_db_connection() as cur:
        await cur.execute(
        '''INSERT INTO 
                workouts (user_id, title, description) 
            VALUES 
                (%s, %s, %s) 
            RETURNING 
                workout_id''', (user_id, workout.title, workout.description))
        result = await cur.fetchone()
        workout_id = result['workout_id']
        
        if workout.exercises:
            await cur.executemany(
        '''INSERT INTO 
                workout_exercises (workout_id, exercise_id, sets, reps, weight, rest_period) 
            VALUES 
                (%s, %s, %s, %s, %s, %s)''', [(workout_id, exercise.exercise_id, exercise.sets, exercise.reps, exercise.rest_period) for exercise in workout.exercises])
            
        return await get_workout_by_id(workout_id)

async def get_workout_by_id(workout_id: UUID) -> Workout:
    async with get_db_connection() as cur:
        await cur.execute(
        '''SELECT 
            w.workout_id,
            w.user_id,
            w.title,
            w.description AS description,
            COALESCE(
                JSON_AGG(
                    JSON_BUILD_OBJECT(
                        'workout_exercise_id', we.workout_exercise_id,
                        'name', e.name,
                        'description', e.description,
                        'sets', we.sets,
                        'reps', we.reps,
                        'weight', we.weight,
                        'rest_period', we.rest_period
                    )
                ) FILTER (WHERE we.workout_exercise_id IS NOT NULL),
                '[]'
            ) AS exercises,
            w.created_at AS created_at,
            w.updated_at AS updated_at
        FROM 
            workouts w
        LEFT JOIN workout_exercises we ON w.workout_id = we.workout_id
        LEFT JOIN exercises e ON we.exercise_id = e.exercise_id
        WHERE
            w.workout_id = %s
        GROUP BY
            w.workout_id;''', (workout_id,))
        return await cur.fetchone()
    
async def get_workouts_by_user(user_id: UUID) -> list[Workout]:
    async with get_db_connection() as cur:
        await cur.execute(
        '''SELECT 
            w.workout_id,
            w.user_id,
            w.title,
            w.description AS description,
            COALESCE(
                JSON_AGG(
                    JSON_BUILD_OBJECT(
                        'workout_exercise_id', we.workout_exercise_id,
                        'name', e.name,
                        'description', e.description,
                        'sets', we.sets,
                        'reps', we.reps,
                        'weight', we.weight,
                        'rest_period', we.rest_period
                    )
                ) FILTER (WHERE we.workout_exercise_id IS NOT NULL),
                '[]'
            ) AS exercises,
            w.created_at AS created_at,
            w.updated_at AS updated_at
        FROM 
            workouts w
        LEFT JOIN workout_exercises we ON w.workout_id = we.workout_id
        LEFT JOIN exercises e ON we.exercise_id = e.exercise_id
        WHERE
            w.user_id = %s
        GROUP BY
            w.workout_id;''', (user_id,))
        return await cur.fetchall()
    
async def add_exercise_to_workout(workout_id: UUID, exercise: AddExercise) -> Workout:
    async with get_db_connection() as cur:
        await cur.execute(
        '''INSERT INTO 
                workout_exercises (workout_id, exercise_id, sets, reps, weight, rest_period) 
            VALUES 
                (%s, %s, %s, %s, %s, %s)''', (workout_id, exercise.exercise_id, exercise.sets, exercise.reps, exercise.weight, exercise.rest_period))
        return await get_workout_by_id(workout_id)
    
async def remove_exercise_from_workout(workout_id: UUID, workout_exercise_id: UUID) -> Workout:
    async with get_db_connection() as cur:
        await cur.execute(
        '''DELETE FROM 
                workout_exercises 
            WHERE 
                workout_id = %s AND workout_exercise_id = %s''', (workout_id, workout_exercise_id))
        return await get_workout_by_id(workout_id)
    
async def delete_workout_by_id(workout_id: UUID) -> None:
    async with get_db_connection() as cur:
        await cur.execute(
        '''DELETE FROM 
                workouts 
            WHERE 
                workout_id = %s''', (workout_id,))
        return None
    
