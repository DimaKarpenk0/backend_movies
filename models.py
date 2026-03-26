from sqlalchemy import Column, Integer, String, Boolean, Float
from database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    director = Column(String, nullable=False)
    releaseYear = Column(Integer)
    rating = Column(Float)
    available = Column(Boolean, default=True)