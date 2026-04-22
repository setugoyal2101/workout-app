from fastapi import APIRouter, Depends, status
from src.tasks import controller
from src.tasks.dtos import Workout_Schema
from src.utils.db import get_db

task_routes = APIRouter(prefix="/workouts")

@task_routes.post("/create-workout")
def create_workout(body: Workout_Schema, db = Depends(get_db)):
  return controller.add_workout(body, db)

@task_routes.get("/get-all-workouts")
def get_all_workouts(db = Depends(get_db)):
  return controller.get_all_workouts(db)

@task_routes.get("/get-workout/{workout_id}")
def get_workout(workout_id: int, db = Depends(get_db)):
  return controller.get_workout(workout_id, db)

@task_routes.get("{workout_type}")
def get_workout_type(workout_type: str, db = Depends(get_db)):
  return controller.get_workout_type(workout_type, db)

@task_routes.put("/update-workout/{workout_id}")
def update_workout(body: Workout_Schema, workout_id: int, db = Depends(get_db)):
  return controller.update_workout(body, workout_id, db)

@task_routes.delete("/delete-workout/{workout_id}")
def delete_workout(workout_id: int, db = Depends(get_db)):
  return controller.delete_workout(workout_id, db)