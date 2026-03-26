from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
from typing import Optional
from auth import SECRET_KEY, ALGORITHM

def get_current_user(authorization: Optional[str] = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        # Authorization должен быть вида "Bearer <token>"
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")