from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base


# Define a SQLAlchemy model
Base = declarative_base()

# Define a table
class Entities(Base):
    __tablename__ = 'entities'
    id = Column(Integer, primary_key=True)
    case_id = Column(Integer)
    name = Column(String)
    current_age = Column(Integer)
    tenure = Column(String)
    smoke_status = Column(String)
    base_rate = Column(Float)