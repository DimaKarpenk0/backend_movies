from pydantic import BaseModel, Field, ConfigDict


class MovieBase(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    director: str = Field(min_length=2, max_length=100)
    release_year: int = Field(ge=1888, le=2100)
    rating: float = Field(gt=0, le=10)
    available: bool


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=100)
    director: str | None = Field(default=None, min_length=2, max_length=100)
    release_year: int | None = Field(default=None, ge=1888, le=2100)
    rating: float | None = Field(default=None, gt=0, le=10)
    available: bool | None = None


class MovieResponse(MovieBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=1, max_length=100)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"