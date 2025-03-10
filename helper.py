from fastapi import FastAPI,Header,Depends,HTTPException
from auth import verify_access_token

def current_user(authorization:str=Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401,detail="Token required")
    token = authorization.split(" ")[1]
    user = verify_access_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user