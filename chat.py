from models import UserQuery
from sqlalchemy.orm import Session
from db import get_db

def save_chat_to_db(chat_data: dict):
    """Saves user query and AI response to the database."""
    print("This is saving chat fn,calling db session ")
    db: Session = next(get_db())  # Get a new database session
    new_chat = UserQuery(
        user_id=chat_data["user_id"],
        query=chat_data["query"],
        response=chat_data["response"]
    )

    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)  # Refresh to get updated data (e.g., ID)
    return new_chat

def get_chat_history(user_id: int):
    
    print("This is chat history")
    db: Session = next(get_db())
    chats = db.query(UserQuery).filter(UserQuery.user_id == user_id).all()#.order_by(UserQuery.id.desc()).all()
    
    return [{"query": chat.query, "response": chat.response,"timestamp":chat.timestamp} for chat in chats]
