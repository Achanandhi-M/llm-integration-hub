from pydantic import BaseModel

# Schema for user registration
class UserCreate(BaseModel):
    username: str
    password: str

# Schema for user login
class UserLogin(BaseModel):
    username: str
    password: str

# Schema for token response
class Token(BaseModel):
    access_token: str
    token_type: str
