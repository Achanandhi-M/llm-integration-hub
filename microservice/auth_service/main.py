from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schema, util
from database_service.database import SessionLocal, engine

# Create all database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register a new user
@app.post("/register", response_model=schema.UserCreate)
def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Hash the password and save the user
    hashed_password = util.hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Exclude the password field before returning the response
    return {
        "username": db_user.username,
        "email": db_user.email,
        # Do not include the password in the response
    }


# User login and return JWT token
@app.post("/login", response_model=schema.Token)
def login(user: schema.UserLogin, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not util.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create and return JWT token
    access_token = util.create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
