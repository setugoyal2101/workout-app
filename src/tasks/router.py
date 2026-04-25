from fastapi import APIRouter, Depends, status
from src.tasks import controller
from src.tasks.dtos import Workout_Schema, Workout_Response_Schema
from src.utils.db import get_db
from src.user.models import UserModel
from src.utils.helpers import is_authenticated

task_routes = APIRouter(prefix="/workouts")

@task_routes.post("/create-workout",response_model = Workout_Response_Schema, status_code=status.HTTP_201_CREATED)
def create_workout(body: Workout_Schema, db = Depends(get_db), user: UserModel = Depends(is_authenticated)):
  return controller.add_workout(body, db, user)

@task_routes.get("/get-all-workouts",response_model = list[Workout_Response_Schema], status_code=status.HTTP_200_OK)
def get_all_workouts(db = Depends(get_db), user: UserModel = Depends(is_authenticated)):
  return controller.get_all_workouts(db, user)

@task_routes.get("/get-workout/{workout_id}",response_model = Workout_Response_Schema, status_code=status.HTTP_200_OK)
def get_workout(workout_id: int, db = Depends(get_db), user: UserModel = Depends(is_authenticated)):
  return controller.get_workout(workout_id, db, user)

@task_routes.get("/get-workout-type/{workout_type}",response_model = Workout_Response_Schema, status_code=status.HTTP_200_OK)
def get_workout_type(workout_type: str, db = Depends(get_db), user: UserModel = Depends(is_authenticated)):
  return controller.get_workout_type(workout_type, db, user)

@task_routes.put("/update-workout/{workout_id}",response_model = Workout_Response_Schema, status_code=status.HTTP_201_CREATED)
def update_workout(body: Workout_Schema, workout_id: int, db = Depends(get_db), user: UserModel = Depends(is_authenticated)):
  return controller.update_workout(body, workout_id, db, user)

@task_routes.delete("/delete-workout/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(workout_id: int, db = Depends(get_db), user: UserModel = Depends(is_authenticated)):
  return controller.delete_workout(workout_id, db, user)