from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from src.utils.db import Base

class WorkoutModel(Base):
  __tablename__ = "workouts"
  id = Column(Integer, primary_key=True)
  workout_name = Column(String)
  workout_type = Column(String)
  duration_minutes = Column(Integer)
  calories_burned = Column(Integer)
  notes = Column(String, nullable=True)
  is_finished = Column(Boolean, default = False)

  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
