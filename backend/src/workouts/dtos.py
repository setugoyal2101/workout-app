from pydantic import BaseModel

class WorkoutSchema(BaseModel):
  workout_name: str
  workout_type: str
  duration_minutes: int
  calories_burned: int
  notes: str | None = None
  is_finished: bool = False
  
class WorkoutResponseSchema(BaseModel):
  id: int
  workout_name: str
  workout_type: str
  duration_minutes: int
  calories_burned: int
  notes: str | None = None
  is_finished: bool = False

  user_id: int | None = 0

  model_config = {
    "from_attributes": True
  }