from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

fake_user = {
    "username": "admin",
    "password": "1234"
}

# Pydantic модель для запроса логина
class LoginRequest(BaseModel):
    username: str
    password: str

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_user(username, password):
    return username == fake_user["username"] and password == fake_user["password"]

@app.post("/auth/login")
def login(request: LoginRequest):
    if verify_user(request.username, request.password):
        token = create_token({"sub": request.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")