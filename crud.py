from sqlalchemy.orm import Session
import models

def get_movies(db: Session):
    return db.query(models.Movie).all()

def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def create_movie(db: Session, movie):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def update_movie(db: Session, movie_id: int, data):
    movie = get_movie(db, movie_id)
    if not movie:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(movie, key, value)
    db.commit()
    db.refresh(movie)
    return movie

def delete_movie(db: Session, movie_id: int):
    movie = get_movie(db, movie_id)
    if not movie:
        return None
    db.delete(movie)
    db.commit()
    return movie