from fastapi import FastAPI, HTTPException,Header,Depends
from pydantic import BaseModel
from register import register_user
from login import user_login
from chat import get_chat_history,save_chat_to_db,getSessionChat
from auth import verify_access_token
from gemini import ask_gemini
# from models import UserQuery
from datetime import datetime
from db import get_db,SessionLocal
import uuid
from sqlalchemy.orm import Session
from helper import current_user


app=FastAPI()

class sessionRequest(BaseModel):
     session_id:str

class ChatRequest(BaseModel):
    query: str
    session_id:str | None=None #can be empty

class RegisterRequest(BaseModel):
    name:str
    email:str
    password:str

class LoginRequest(BaseModel):
    email:str
    password:str


@app.get("/")
def home():
    return {"message":"This is fastAPI chatapp"}

# User Registration Endpoint
@app.post("/register")
def register(data: RegisterRequest):
    result = register_user(data.name, data.email, data.password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


# User Login Endpoint
@app.post("/login")
def login(data: LoginRequest):
    result = user_login(data.email, data.password)
    print("login result = ",result)
    if "error" in result:
        raise HTTPException(status_code=401, detail=result["error"])
    return result

# modify it for chAT with session id
@app.post("/chat")
def chat(
     request:ChatRequest,
     user:dict=Depends(current_user),#calling fn from helper which can validate aT and return user info
     session_id: str = Header(None),
     db:Session=Depends(get_db)#Calls the get_db() function when the route is accessed,we don't haave to call db manually
     ):
    print("session_id ",session_id)
    if not session_id:
         session_id=str(uuid.uuid4())

    # get last 10 chats
    print("chat history function called.")
    print("session_id is =",session_id)
    
    chat=get_chat_history(user['id'],session_id)

    print("chat his is=",chat)
    chat_history=[]
    for q in chat:
        chat_history.append({"role": "user", "parts": [{"text": q['query']}]})
        chat_history.append({"role": "model", "parts": [{"text": q['response']}]})
    
    # add new question
    chat_history.append({"role": "user", "parts": [{"text": request.query}]})
    print('chat history')
    response = ask_gemini(chat_history)  
    print("gemini response is ",response)
    
    chat_entry = save_chat_to_db({
        "user_id": user['id'],
        "session_id":session_id,
        "query": request.query,
        "response": response,
        "timestamp":datetime.utcnow()
    })

    return{
        "session_id":session_id,
        "user":request.query,
        "gemini":response,
        # "timestamp": datetime.utcnow().isoformat(),
        "time":datetime.utcnow().strftime("%I:%M %p, %d %B %Y"),
        "full_chat_history": chat_history
            }


# all chat history of user with different sessions
# @app.get('/chat/history')
# def get_history(
#      user:dict=Depends(current_user),
#     #  session_id:str=Header(None)
#      ):
#     chat_history=get_chat_history(user['id'])

#     for chat in chat_history:
#         print(f"Query: {chat['query']}\nResponse: {chat['response']}\n Time:{chat['timestamp']}")
    
#     history_list=[
#          {
#              "session_id":chat['session_id'],
#               "query":chat['query'],
#               "response":chat['response'],
#               "timestamp":chat['timestamp'].strftime("%I:%M %p, %d %B %Y")
#                 # "timestamp": datetime.strptime(chat['timestamp'], "%Y-%m-%dT%H:%M:%S.%f")
#               }
#               for chat in chat_history
#               ]
#     return {
#          "chat_history":history_list
#     }

@app.get('/chat/history')
def get_history(user: dict = Depends(current_user)):
    chat_history = get_chat_history(user['id'])

    
    # for session in chat_history:
    #     print(f"Session ID: {session['session_id']}")
    #     for chat in session['chats']:
    #         print(f"Query: {chat['query']}\nResponse: {chat['response']}\nTime: {chat['timestamp']}")
    
    return {"chat_history": chat_history}
         
         
# api call for session (take user access token and show session) so that user can see its session
@app.get("/chat/history/session")
def user_session(
     session_id:str=Header(None),
     user:dict=Depends(current_user),
     db:Session=Depends(get_db)):

     chat_history=getSessionChat(user['id'],session_id)
     
     print("chat history is ",chat_history)
     history_list=[
         {
              "query":chat['query'],
              "response":chat['response'],
              "timestamp":chat['timestamp'].strftime("%I:%M %p, %d %B %Y")
            
              }
              for chat in chat_history
              ]
     return {
         "chat_history":history_list
        }
    
     
     