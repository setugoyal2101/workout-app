from backend.src.workouts.dtos import WorkoutSchema
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.src.workouts.models import WorkoutModel
from fastapi import HTTPException, Response, status
from backend.src.user.models import UserModel


def add_workout(body: WorkoutSchema, db: Session, user: UserModel):
  data = body.model_dump()
  #new_workout = WorkoutModel(title = data["title"], description = data["description"], is_finished = data["is_finished"])
  # This does the EXACT SAME THING as your 3 lines of code:
  new_workout = WorkoutModel(**data)
  new_workout.user_id = user.id
  db.add(new_workout)
  db.commit()
  db.refresh(new_workout)
  
  return new_workout

def get_all_workouts(db: Session, user: UserModel):
  return user.workouts

def get_workout(workout_id: int, db: Session, user: UserModel):
  one_workout: WorkoutModel =  db.query(WorkoutModel).filter(WorkoutModel.id == workout_id).first()
  if not one_workout:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout ID is incorrect")
  
  if one_workout.user_id != user.id: #type: ignore
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to view this workout")
  
  return one_workout

def get_workout_type(workout_type: str, db: Session, user: UserModel):
  workout: list[WorkoutModel] = db.query(WorkoutModel).filter(WorkoutModel.workout_type == workout_type, WorkoutModel.user_id == user.id).all()
  if not workout:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout type not found")
  
  if workout.user_id != user.id: #type: ignore
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to view this workout type")
  
  return workout

def update_workout(body: WorkoutSchema, workout_id: int, db: Session, user: UserModel):
  workout: WorkoutModel = db.query(WorkoutModel).filter(WorkoutModel.id == workout_id).first()
  if not workout:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout ID is incorrect")
  
  if workout.user_id != user.id: #type: ignore
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this workout")
  
  body = body.model_dump()
  for key, value in body.items():
    setattr(workout, key, value)
  
  db.add(workout)
  db.commit()
  db.refresh(workout)

  return workout

def delete_workout(workout_id: int, db: Session, user: UserModel):
  workout: WorkoutModel = db.query(WorkoutModel).filter(WorkoutModel.id == workout_id).first()
  if not workout:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout ID not found")
  
  if workout.user_id != user.id: #type: ignore
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this workout")
  
  db.delete(workout)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)

def is_finished(workout_finished: bool, db: Session, user: UserModel):
  workout: list[WorkoutModel] = db.query(WorkoutModel).filter(WorkoutModel.user_id == user.id, WorkoutModel.is_finished == workout_finished).all()

  return workout
    
def calorie_range_calculator(db: Session, user: UserModel, calorie_min: int = None, calorie_max: int = None):
  query = db.query(WorkoutModel).filter(WorkoutModel.user_id == user.id)

  if calorie_min is not None:
    query = query.filter(WorkoutModel.calories_burned >= calorie_min)

  if calorie_max is not None:
    query = query.filter(WorkoutModel.calories_burned <= calorie_max)

  total_cals = query.with_entities(func.sum(WorkoutModel.calories_burned)).scalar()

  return total_cals or 0

    




  


  