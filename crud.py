from sqlalchemy.orm import Session
import models
import schemas


def get_movies(db: Session):
    return db.query(models.Movie).all()


def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(**movie.model_dump())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def replace_movie(db: Session, movie_id: int, data: schemas.MovieCreate):
    movie = get_movie(db, movie_id)
    if not movie:
        return None

    for key, value in data.model_dump().items():
        setattr(movie, key, value)

    db.commit()
    db.refresh(movie)
    return movie


def update_movie(db: Session, movie_id: int, data: schemas.MovieUpdate):
    movie = get_movie(db, movie_id)
    if not movie:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
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