from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy.orm import relationship
from Base import Base
from FilmGenres import film_genres


class FilmORM(Base):
    __tablename__ = 'films'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    creation_date = Column(Date)
    file_link = Column(String(255))

    genres = relationship("GenreORM", secondary=film_genres, back_populates="films")
