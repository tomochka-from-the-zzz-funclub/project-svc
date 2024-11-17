from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.db.models.Base import Base
from app.infrastructure.db.models.FilmGenres import film_genres


class GenreORM(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    films = relationship("FilmORM", secondary=film_genres, back_populates="genres")