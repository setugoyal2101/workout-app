from fastapi import FastAPI
from backend.src.utils.db import Base, engine
from backend.src.workouts.router import workout_routes
from backend.src.user.router import user_routes
from fastapi.middleware.cors import CORSMiddleware





app = FastAPI(title="Fitness tracker application")
app.include_router(workout_routes)
app.include_router(user_routes)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, you'd change this to your specific URL
    allow_methods=["*"],
    allow_headers=["*"],
)
