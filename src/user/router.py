from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.dtos import UserSchema, UserResponseSchema, LoginResponseSchema, LoginSchema
from src.user import controller

user_routes = APIRouter(prefix="/user")

@user_routes.post("/create-user", response_model=UserResponseSchema)
def create_user(body: UserSchema, db: Session = Depends(get_db)):
  return controller.create_user(body, db)

@user_routes.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponseSchema)
def login_user(body: LoginSchema, db: Session = Depends(get_db)):
  return controller.login_user(body, db)

@user_routes.get("/is-authenticated", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
def is_authenticated(request: Request, db: Session = Depends(get_db)):
  return controller.is_authenticated(request, db)