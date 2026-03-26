from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas, crud
from database import engine, SessionLocal
from auth import create_token, verify_user
from dependencies import get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Подключение БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Авторизация
@app.post("/auth/login")
def login(username: str, password: str):
    if not verify_user(username, password):
        raise HTTPException(status_code=401, detail="Wrong credentials")
    token = create_token({"sub": username})
    return {"access_token": token}

# GET all
@app.get("/movies")
def get_movies(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.get_movies(db)

# GET by id
@app.get("/movies/{id}")
def get_movie(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    movie = crud.get_movie(db, id)
    if not movie:
        raise HTTPException(status_code=404, detail="Not found")
    return movie

# POST
@app.post("/movies")
def create(movie: schemas.MovieCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.create_movie(db, movie)

# PUT / PATCH
@app.patch("/movies/{id}")
def update(id: int, data: schemas.MovieUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    movie = crud.update_movie(db, id, data)
    if not movie:
        raise HTTPException(status_code=404, detail="Not found")
    return movie

# DELETE
@app.delete("/movies/{id}")
def delete(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    movie = crud.delete_movie(db, id)
    if not movie:
        raise HTTPException(status_code=404, detail="Not found")
    return {"message": "Deleted"}