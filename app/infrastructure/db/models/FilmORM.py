from __future__ import annotations

from typing import List, TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy.orm import relationship, Mapped

from app.infrastructure.db.models.Base import Base
from app.infrastructure.db.models.FilmGenres import film_genres


if TYPE_CHECKING:
    from app.infrastructure.db.models.GenreORM import GenreORM


class FilmORM(Base):
    __tablename__ = 'films'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    creation_date = Column(Date)
    file_link = Column(String(255))

    genres: Mapped[List[GenreORM]] = relationship("GenreORM", secondary=film_genres, back_populates="films", lazy="noload")
