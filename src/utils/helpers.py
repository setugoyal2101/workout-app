from fastapi import Request, HTTPException, status, Depends
from src.user.models import UserModel
from sqlalchemy.orm import Session
from src.utils.settings import settings
from jwt.exceptions import InvalidTokenError
from src.utils.db import get_db
import jwt

def is_authenticated(request: Request, db: Session = Depends(get_db)):   
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