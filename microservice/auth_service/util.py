import os
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import HTTPException

# Load environment variables from .env file
load_dotenv()

# CryptContext for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Read values from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")  # Default fallback in case of missing env variable
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Hash password function
def hash_password(password: str) -> str:
    """
    Hash a plain password using bcrypt algorithm.
    """
    return pwd_context.hash(password)

# Verify password function
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if the plain password matches the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

# JWT token creation function
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token with the specified data and expiration.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# JWT token verification function
def verify_token(token: str) -> str:
    """
    Verify the JWT token and extract the user info (subject) from it.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]  # Return the user ID or username
    except JWTError:
        return None

# OAuth2 password bearer class for token extraction
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to get the current user from the token
def get_current_user(token: str = oauth2_scheme) -> str:
    """
    Extract and verify the user from the JWT token passed in the Authorization header.
    """
    user = verify_token(token)  # Verify token using the verify_token function
    
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return user
