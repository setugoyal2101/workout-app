from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from backend.src.utils.db import get_db
from backend.src.user.dtos import UserSchema, UserResponseSchema, LoginResponseSchema, LoginSchema
from backend.src.user import controller
from backend.src.utils import helpers
from backend.src.user.models import UserModel

user_routes = APIRouter(prefix="/user")

@user_routes.post("/", response_model=UserResponseSchema)
def create_user(body: UserSchema, db: Session = Depends(get_db)):
  return controller.create_user(body, db)

@user_routes.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponseSchema)
def login_user(body: LoginSchema, db: Session = Depends(get_db)):
  return controller.login_user(body, db)

@user_routes.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
def get_current_user(user: UserModel = Depends(helpers.is_authenticated)):
  return user

