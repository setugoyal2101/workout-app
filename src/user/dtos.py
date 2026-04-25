from pydantic import BaseModel

class UserSchema(BaseModel):
  name: str
  email: str
  password: str

class UserResponseSchema(BaseModel):
  name: str
  email: str

class LoginSchema(BaseModel):
  email: str
  password: str

class LoginResponseSchema(BaseModel):
  access_token: str
  token_type: str = "bearer"