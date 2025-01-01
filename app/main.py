from fastapi import FastAPI
from app.routes.users import user_router
from app.routes.workouts import workout_router
from app.routes.exercise import exercise_router
from app.routes.schedule_workout import schedule_router
from app.routes.workout_report import report_router

app = FastAPI(title="Exercise API", description="API for exercises", version="0.1")

app.include_router(user_router)
app.include_router(exercise_router)
app.include_router(workout_router)
app.include_router(schedule_router)
app.include_router(report_router)

