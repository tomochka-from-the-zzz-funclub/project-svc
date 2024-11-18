from __future__ import annotations

from typing import List, TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped

from app.infrastructure.db.models.Base import Base
from app.infrastructure.db.models.FilmGenres import film_genres

if TYPE_CHECKING:
    from app.infrastructure.db.models.FilmORM import FilmORM

class GenreORM(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    films: Mapped[List[FilmORM]] = relationship("FilmORM", secondary=film_genres, back_populates="genres")