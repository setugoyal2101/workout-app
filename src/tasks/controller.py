from src.tasks.dtos import Workout_Schema
from sqlalchemy.orm import Session
from src.tasks.models import WorkoutModel
from fastapi import HTTPException

def add_workout(body: Workout_Schema, db: Session):
  data = body.model_dump()
  #new_workout = WorkoutModel(title = data["title"], description = data["description"], is_finished = data["is_finished"])
  # This does the EXACT SAME THING as your 3 lines of code:
  new_workout = WorkoutModel(**data)
  db.add(new_workout)
  db.commit()
  db.refresh(new_workout)
  
  return {
    "status": "workout created successfully", "data": new_workout
  }

def get_all_workouts(db: Session):
  all_workouts = db.query(WorkoutModel).all()
  return {"status": "workouts retrieved successfully", "data": all_workouts}

def get_workout(workout_id: int, db: Session):
  one_workout =  db.query(WorkoutModel).filter(WorkoutModel.id == workout_id).first()
  if not one_workout:
    raise HTTPException(404, detail="Workout ID is incorrect")
  
  return {"status": "workout retrieved successfully", "data": one_workout}

def get_workout_type(workout_type: str, db: Session):
  workout_type = db.query(WorkoutModel).filter(WorkoutModel.workout_type == workout_type).first() 

def update_workout(body: Workout_Schema, workout_id: int, db: Session):
  workout = db.query(WorkoutModel).filter(WorkoutModel.id == workout_id).first()
  if not workout:
    raise HTTPException(404, "Workout ID is incorrect")
  
  body = body.model_dump()
  for key, value in body.items():
    setattr(workout, key, value)
  
  db.add(workout)
  db.commit()
  db.refresh(workout)

  return {"status": "Workout updated successfully", "data": workout}

def delete_workout(workout_id: int, db: Session):
  workout = db.query(WorkoutModel).get(workout_id)
  if not workout:
    raise HTTPException(404, "Workout ID not found")
  
  db.delete(workout)
  db.commit()

  return None





  