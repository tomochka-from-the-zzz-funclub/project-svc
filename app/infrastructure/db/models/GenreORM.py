from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Base import Base
from FilmGenres import film_genres

class GenreORM(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    films = relationship("FilmORM", secondary=film_genres, back_populates="genres")