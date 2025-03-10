from sqlalchemy import create_engine,Integer,Column,String,ForeignKey,Text,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from datetime import datetime



Base=declarative_base()

class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(100),nullable=False)
    email=Column(String(100),unique=True,nullable=False)
    password=Column(String(200),nullable=False)

    # define relation with UserQuery Table(1->Many)
    queries=relationship("UserQuery",back_populates='user',cascade='all, delete-orphan')

class UserQuery(Base):
    __tablename__='user_queries'
    id=Column(Integer,primary_key=True,autoincrement=True)
    user_id=Column(Integer,ForeignKey('users.id'),nullable=False)
    # adding session id
    session_id=Column(String,nullable=False)
    query=Column(Text,nullable=False)
    response=Column(Text,nullable=False)
    timestamp=Column(DateTime,default=datetime.utcnow)#creting date time for each user query
    
    # define relationship
    user=relationship("User",back_populates='queries')