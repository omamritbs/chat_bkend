from fastapi import FastAPI, HTTPException,Header
from pydantic import BaseModel
from register import register_user
from login import user_login
from chat import get_chat_history,save_chat_to_db
from auth import create_access_token,verify_access_token
from gemini import ask_gemini
from models import UserQuery
from datetime import datetime


app=FastAPI()

class ChatRequest(BaseModel):
    query: str

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


@app.post("/chat")
def chat(request:ChatRequest,authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token required")
    token = authorization.split(" ")[1]
    user = verify_access_token(token)

    print("user id is",user)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    # get last 10 chats
    print("chat history function called.")
    chat=get_chat_history(user['id'])
    print('chat history is ',chat)
    chat_history=[]
    for q in chat:
        chat_history.append({"role": "user", "parts": [{"text": q['query']}]})
        chat_history.append({"role": "model", "parts": [{"text": q['response']}]})
    
    # add new question
    chat_history.append({"role": "user", "parts": [{"text": request.query}]})

    response = ask_gemini(chat_history)  

    chat_entry = save_chat_to_db({
        "user_id": user['id'],
        "query": request.query,
        "response": response,
        "timestamp":datetime.utcnow()
    })
    return{"user":request.query,
           "gemini":response,
        #    "timestamp": datetime.utcnow().isoformat(),
            "time":datetime.utcnow().strftime("%I:%M %p, %d %B %Y"),
            # "full_chat_history": chat_history
            }


@app.get('/chat/history')
def get_history(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token required")
    token = authorization.split(" ")[1]
    user = verify_access_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    chat_history=get_chat_history(user['id'])

    for chat in chat_history:
        print(f"Query: {chat['query']}\nResponse: {chat['response']}\n Time:{chat['timestamp']}")
    
    history_list=[
         {
              "query":chat['query'],
              "response":chat['response'],
              "timestamp":chat['timestamp'].strftime("%I:%M %p, %d %B %Y")
                # "timestamp": datetime.strptime(chat['timestamp'], "%Y-%m-%dT%H:%M:%S.%f")
              }
              for chat in chat_history
              ]
    return {
         "chat_history":history_list
    }
         
         


