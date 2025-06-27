from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Float, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import random



# Create an engine
engine = create_engine('sqlite:///insurance_data.db')

# Create a SQLAlchemy session
Session = sessionmaker(bind=engine)
session = Session()

# Define a SQLAlchemy model
Base = declarative_base()

class Entities(Base):
    __tablename__ = 'entities'
    id = Column(Integer, primary_key=True)
    case_id = Column(Integer)
    name = Column(String)
    current_age = Column(Integer)
    tenure = Column(String)
    smoke_status = Column(Boolean)
    base_rate = Column(Float)
    

Base.metadata.create_all(engine)

# Generate a random 5-digit number
random_number = random.randint(10000, 99999)

session.add(Entities(case_id = random_number, name='XYZ', current_age=30, tenure=2, smoke_status=True))
# session.add(Entities(name='PQR', current_age=50, tenure=1, smoke_status=False))
session.commit()