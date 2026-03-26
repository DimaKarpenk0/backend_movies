from fastapi import FastAPI, Depends, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import models, schemas, crud
from database import engine, SessionLocal
from auth import create_token, verify_user
from dependencies import get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movies API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def api_error(status_code: int, error: str, message: str, details=None):
    payload = {
        "status": status_code,
        "error": error,
        "message": message,
    }
    if details is not None:
        payload["details"] = details
    return JSONResponse(status_code=status_code, content=payload)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()

    is_bad_request = any(
        err.get("type") in {"json_invalid", "json_parsing", "json_decode"}
        or (err.get("loc") and err["loc"][0] in {"path", "query"})
        for err in errors
    )

    if is_bad_request:
        return api_error(
            400,
            "Bad Request",
            "Incorrect JSON, path parameter, or query parameter format",
            errors,
        )

    return api_error(
        422,
        "Unprocessable Entity",
        "Validation failed",
        errors,
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    titles = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        500: "Internal Server Error",
    }
    return api_error(
        exc.status_code,
        titles.get(exc.status_code, "HTTP Error"),
        str(exc.detail),
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return api_error(
        500,
        "Internal Server Error",
        "Database error",
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return api_error(
        500,
        "Internal Server Error",
        "Unexpected server error",
    )


@app.post("/auth/login", response_model=schemas.TokenResponse)
def login(request: schemas.LoginRequest):
    if not verify_user(request.username, request.password):
        return api_error(401, "Unauthorized", "Wrong credentials")

    token = create_token({"sub": request.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/movies", response_model=list[schemas.MovieResponse])
def get_movies(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return crud.get_movies(db)


@app.get("/movies/{movie_id}", response_model=schemas.MovieResponse)
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    movie = crud.get_movie(db, movie_id)
    if not movie:
        return api_error(404, "Not Found", "Movie not found")
    return movie


@app.post("/movies", response_model=schemas.MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(
    movie: schemas.MovieCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return crud.create_movie(db, movie)


@app.put("/movies/{movie_id}", response_model=schemas.MovieResponse)
def replace_movie(
    movie_id: int,
    data: schemas.MovieCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    movie = crud.replace_movie(db, movie_id, data)
    if not movie:
        return api_error(404, "Not Found", "Movie not found")
    return movie


@app.patch("/movies/{movie_id}", response_model=schemas.MovieResponse)
def update_movie(
    movie_id: int,
    data: schemas.MovieUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    movie = crud.update_movie(db, movie_id, data)
    if not movie:
        return api_error(404, "Not Found", "Movie not found")
    return movie


@app.delete("/movies/{movie_id}")
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    movie = crud.delete_movie(db, movie_id)
    if not movie:
        return api_error(404, "Not Found", "Movie not found")
    return {"message": "Deleted"}