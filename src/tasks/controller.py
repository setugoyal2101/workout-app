from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException

def add_workout(body: TaskSchema, db: Session):
  data = body.model_dump()
  #new_workout = TaskModel(ritle = data["title"], description = data["description"], is_completed = data["description"])
  # This does the EXACT SAME THING as your 3 lines of code:
  new_workout = TaskModel(**data)

  db.add(new_workout)
  db.commit()
  db.refresh(new_workout)
  
  return {
    "status": "workout created successfully", "data": new_workout
  }

def get_workout(workout_id: int, db: Session):
  one_workout =  db.query(TaskModel).filter(TaskModel.id == workout_id).first()
  if not one_workout:
    raise HTTPException(404, detail="Workout ID is incorrect")
  
  return {"status": "workout retrieved successfully", "data": one_workout}

def update_workout(body: TaskSchema, workout_id: int, db: Session):
  workout = db.query(TaskModel).get(workout_id)
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
  workout = db.query(TaskModel).get(workout_id)
  if not workout:
    raise HTTPException(404, "Workout ID not found")
  
  db.delete(workout)
  db.commit()

  return None





  