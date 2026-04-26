from sqlalchemy import Column, Integer, String
from backend.src.utils.db import Base

class UserModel(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True)
  name = Column(String)
  email = Column(String, nullable=False, unique=True)
  hash_password = Column(String, nullable=False)