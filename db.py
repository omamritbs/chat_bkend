from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User,UserQuery
import psycopg2

# define db info
hostname='localhost'
database='postgres'
username='postgres'
pwd='1234567890'
port_id=5432

# define db url
DATABASE_URL=f"postgresql+psycopg2://{username}:{pwd}@{hostname}:{port_id}/{database}"

# create engine
engine=create_engine(DATABASE_URL)

# check connection
try:
    if engine.connect():
        print("database connected")
except Exception as e:
    print("Error in connection :",e)

# define ORM 
Base=declarative_base()


# create a fatory session(fresh start after each call) using sessionmaker and bind it to db
SessionLocal=sessionmaker(bind=engine)
session=SessionLocal()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# defined the orm now creating tables
Base.metadata.create_all(engine)
print('Table sucessfully created')


