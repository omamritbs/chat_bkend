from models import UserQuery
from sqlalchemy.orm import Session
from db import get_db
from collections import defaultdict

# save query response to database
def save_chat_to_db(chat_data: dict):
    print("This is saving chat fn,calling db session ")
    db: Session = next(get_db())  # Get a new database session
    new_chat = UserQuery(
        user_id=chat_data["user_id"],
        session_id=chat_data['session_id'],
        query=chat_data["query"],
        response=chat_data["response"],
        timestamp=chat_data['timestamp']
    )
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)  # Refresh to get updated data 
    return new_chat

def get_chat_history(user_id: int):
    print("This is chat history")
    db: Session = next(get_db())
    chats = db.query(UserQuery).filter(UserQuery.user_id == user_id).all()
    
    chat_sessions = defaultdict(list)

    print("chat session =",chat_sessions)
    for chat in chats:
        chat_sessions[chat.session_id].append({
            "query": chat.query, 
            "response": chat.response,
            "timestamp": chat.timestamp.strftime("%I:%M %p, %d %B %Y")
        })
    
    return [
        {
            "session_id": session_id, 
            "chats": chat_list
            }
              for session_id, chat_list in chat_sessions.items()]

def getSessionChat(user_id:int,session_id:str):
    db: Session = next(get_db())
    chats=db.query(UserQuery).filter(UserQuery.user_id==user_id,UserQuery.session_id==session_id).all()
    return [
            {
            "session_id":session_id,
            "query": chat.query, 
            "response": chat.response,
            "timestamp":chat.timestamp
            } 
            for chat in chats]
    
