from fastapi import APIRouter, Depends, status
from backend.src.workouts import controller
from backend.src.workouts.dtos import WorkoutSchema, WorkoutResponseSchema
from backend.src.utils.db import get_db
from backend.src.user.models import UserModel
from backend.src.utils.helpers import is_authenticated
from sqlalchemy.orm import Session

workout_routes = APIRouter(prefix="/workouts")

@workout_routes.post("/",response_model = WorkoutResponseSchema, status_code=status.HTTP_201_CREATED)
def create_workout(body: WorkoutSchema, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
  return controller.add_workout(body, db, user)

@workout_routes.get("/all",response_model = list[WorkoutResponseSchema], status_code=status.HTTP_200_OK)
def get_all_workouts(db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
  return controller.get_all_workouts(db, user)

@workout_routes.get("/view/{workout_id}",response_model = WorkoutResponseSchema, status_code=status.HTTP_200_OK)
def get_workout(workout_id: int, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
  return controller.get_workout(workout_id, db, user)

@workout_routes.get("/type/{workout_type}",response_model = list[WorkoutResponseSchema], status_code=status.HTTP_200_OK)
def get_workout_type(workout_type: str, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
  return controller.get_workout_type(workout_type, db, user)

@workout_routes.put("/update/{workout_id}",response_model = WorkoutResponseSchema, status_code=status.HTTP_201_CREATED)
def update_workout(body: WorkoutSchema, workout_id: int, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
  return controller.update_workout(body, workout_id, db, user)

@workout_routes.delete("/delete/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(workout_id: int, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
  return controller.delete_workout(workout_id, db, user)

@workout_routes.get("/is-finished/{workout_finished}", response_model= list[WorkoutResponseSchema], status_code=status.HTTP_200_OK)
def is_finished(workout_finished: bool, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
  return controller.is_finished(workout_finished, db, user)

@workout_routes.get("/calorie-range", status_code=status.HTTP_200_OK)
def calorie_range_calculator(
    calorie_min: int | None = None,
    calorie_max: int | None = None,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated)
):
  return controller.calorie_range_calculator(db, user, calorie_min, calorie_max)