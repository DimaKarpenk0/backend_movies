from pydantic import BaseModel, Field

class MovieBase(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    director: str
    releaseYear: int
    rating: float = Field(gt=0, lt=10)
    available: bool

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: str | None = None
    director: str | None = None
    releaseYear: int | None = None
    rating: float | None = None
    available: bool | None = None

class MovieResponse(MovieBase):
    id: int

    class Config:
        orm_mode = True