from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import model, database
from auth_service import schema

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Store query result in the database
@app.post("/store_query_result")
def store_query_result(query: str, result: str, db: Session = Depends(get_db)):
    db_query = models.QueryResult(query=query, result=result)
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query

# Get query result from the database
@app.get("/get_query_result/{query}")
def get_query_result(query: str, db: Session = Depends(get_db)):
    db_query = db.query(models.QueryResult).filter(models.QueryResult.query == query).first()
    if not db_query:
        raise HTTPException(status_code=404, detail="Query not found")
    return db_query
