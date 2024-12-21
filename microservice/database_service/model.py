from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Model to store query results
class QueryResult(Base):
    __tablename__ = 'query_results'
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, unique=True, index=True)
    result = Column(String)
