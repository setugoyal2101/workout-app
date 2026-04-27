from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from backend.src.utils.db import Base
from sqlalchemy.orm import relationship

class WorkoutModel(Base):
  __tablename__ = "workouts"
  id = Column(Integer, primary_key=True)
  workout_name = Column(String, nullable=False)
  workout_type = Column(String, nullable=False)
  duration_minutes = Column(Integer, nullable=False)
  calories_burned = Column(Integer, nullable=False)
  notes = Column(String, nullable=True)
  is_finished = Column(Boolean, default = False)

  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
  owner = relationship("UserModel", back_populates="workouts")
