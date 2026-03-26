from sqlalchemy import Column, Integer, String, Boolean, Float
from database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    director = Column(String(100), nullable=False)
    release_year = Column('releaseYear', Integer, nullable=False)
    rating = Column(Float, nullable=False)
    available = Column(Boolean, default=True, nullable=False)