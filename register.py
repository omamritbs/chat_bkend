from db import User
from db import SessionLocal
import bcrypt
from sqlalchemy.exc import IntegrityError

def hash_password(password):
    # hash password using bcrypt
    salt=bcrypt.gensalt()
    # hashed=bcrypt.hashpw(password.encode(),salt)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def register_user(name:str,email:str,pwd:str):
    session=SessionLocal()
    try:
        print("hashing your pwd")
        hash_pwd=hash_password(pwd)
        print("password hashed")
        new_user=User(name=name,email=email,password=hash_pwd)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        print("new user= ",new_user)
        return{f"New user {name} rgistered sucessfully"}

    except IntegrityError: #use when db constraint like unique key violated
        session.rollback() #clears the error and resets the session so it can continue running
        return{"Error: Email already exists."}
    except Exception as e:
        return{"Registration error:", str(e)}
    finally:
        session.close()