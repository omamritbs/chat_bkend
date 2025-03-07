import bcrypt
from db import User
from db import SessionLocal
from auth import create_access_token,verify_access_token
from datetime import timedelta


ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_pwd:str,hash_pwd:str) ->bool:
    return bcrypt.checkpw(plain_pwd.encode('utf-8'),hash_pwd.encode('utf-8'))

def user_login(email:str,pwd:str):
    session=SessionLocal()
    try:
        user=session.query(User).filter(User.email==email).first()
        print("user is ",user.name)
        if not user:
            return {"error": "User not found. Please register first."}
        hashed_password = str(user.password)  # Convert to string if needed

        if not verify_password(pwd, hashed_password):
            return {"error": "Invalid email or password."}
        print("calling access token fn....")
        token = create_access_token(data={'id':user.id,"name": user.name, "email": user.email})
        # ,expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),)
        return {"access_token": token, "message": f"Login successful! Welcome, {user.name}"}
    
    except Exception as e:
        print("Login error:", e)
    finally:
        session.close()


