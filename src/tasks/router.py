from fastapi import APIRouter, Depends
from src.tasks import controller
from src.tasks.dtos import TaskSchema
from src.utils.db import get_db

task_routes = APIRouter(prefix="/workouts")

@task_routes.post("/create-workout")
def create_workout(body: TaskSchema, db = Depends(get_db)):
  return controller.add_workout(body, db)

@task_routes.get("/get-workout/{workout_id}")
def get_workout(workout_id: int, db = Depends(get_db)):
  return controller.get_workout(workout_id, db)

@task_routes.put("/update-workout/{workout_id}")
def update_workout(body: TaskSchema, workout_id: int, db = Depends(get_db)):
  return controller.update_workout(body, workout_id, db)

@task_routes.delete("/delete-workout/{workout_id}")
def delete_workout(workout_id: int, db = Depends(get_db)):
  return controller.delete_workout(workout_id, db)