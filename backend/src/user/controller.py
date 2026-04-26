from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session
from backend.src.user.models import UserModel  
from backend.src.user.dtos import UserSchema, LoginSchema
from backend.src.utils.settings import settings
from pwdlib import PasswordHash
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError

password_hash = PasswordHash.recommended()

def get_password_hash(password: str):
  return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str):
  return password_hash.verify(plain_password, hashed_password)

def create_user(body: UserSchema, db: Session):
  is_user = db.query(UserModel).filter(UserModel.email == body.email).first()

  if is_user:
    raise HTTPException(400, detail="Email already exists")
  
  hash_password = get_password_hash(body.password)

  new_user = UserModel(
    name = body.name,
    email = body.email,
    hash_password = hash_password,
  )

  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  return new_user

def login_user(body: LoginSchema, db: Session):
  user: UserModel = db.query(UserModel).filter(UserModel.email == body.email).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "You're not authorised")
  
  if not verify_password(body.password, str(user.hash_password)):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You're not authorised")
  
  exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)

  token = jwt.encode({"user_id": user.id, "exp": exp_time}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
  
  return {
    "access_token": token,
    "token_type": "bearer"
    }

def is_authenticated(request: Request, db: Session):   
  try:
    token = request.headers.get("Authorization")
    if not token:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You're not authorised")
    
    token = token.split(" ")[1]

    token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id = token.get("user_id")
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You're not authorised")
    return user

  except InvalidTokenError:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You're not authorised")