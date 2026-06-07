from pydantic import BaseModel, EmailStr

# Schema for new user create
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"

# Schema for user login
class UserLogin(BaseModel):
    username: str
    password: str