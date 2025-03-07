import jwt
import datetime
from datetime import datetime, timedelta


SECRET_KEY='my_secret_key'
ALGORITHM='HS256'

def create_access_token(data: dict):#, expires_delta: timedelta):
    to_encode = data.copy()
    # print("to encode ",to_encode)
    # expire = datetime.utcnow() + expires_delta
    # to_encode.update({"exp": expire})
    # print('encoded ',to_encode)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print("payload is ",payload)
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
    
