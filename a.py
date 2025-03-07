# import bcrypt

# # Function to hash a password
# def hash_password(password: str) -> str:
#     salt = bcrypt.gensalt()  # Generate a salt
#     print(salt)
#     hashed = bcrypt.hashpw(password.encode(), salt)  # Hash the password
#     return hashed

# # Example usage
# password = "my_secure_password"
# hashed_password = hash_password(password)
# print("Hashed Password:", hashed_password)
# a='$2b$12$hec5r499eQe2O5ja0GN7Aesf7l6YW3IvsNdG4r218sXyFq09wJI'
# print(len(a))


# # User Login Endpoint
# @app.post("/login")
# def login(data: LoginRequest):
#     result = user_login(data.email, data.password)
#     print("login result = ",result)
#     if "error" in result:
#         raise HTTPException(status_code=401, detail=result["error"])
#     return result



# # login page

# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# def verify_password(plain_pwd:str,hash_pwd:str) ->bool:
#     return bcrypt.checkpw(plain_pwd.encode('utf-8'),hash_pwd.encode('utf-8'))

# def user_login(email:str,pwd:str):
#     session=SessionLocal()
#     try:
#         user=session.query(User).filter(User.email==email).first()
#         print(user)
#         if not user:
#             return {"error": "User not found. Please register first."}
#         hashed_password = str(user.password)  # Convert to string if needed

#         if not verify_password(pwd, hashed_password):
#             return {"error": "Invalid email or password."}
        
#         token = create_access_token(data={'id':user.id,"name": user.name, "email": user["email"]},
#         expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),)
#         return {"access_token": token, "message": f"Login successful! Welcome, {user.name}"}
    
#     except Exception as e:
#         print("Login error:", e)
#     finally:
#         session.close()

# # token generate page

# def create_access_token(data: dict, expires_delta: timedelta):
#     """Generate JWT token with user details."""
#     to_encode = data.copy()
#     expire = datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# TypeError: argument of type 'NoneType' is not iterable

a={'id': 3, 'name': 'rahul', 'email': 'rahul@gmail.com'}
print(a['name'])
# print(a.name)
a.append({'name':'om'})
print(a)