from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

fake_user = {
    "username": "admin",
    "password": "1234"
}


def create_token(data: dict) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_user(username: str, password: str) -> bool:
    return username == fake_user["username"] and password == fake_user["password"]