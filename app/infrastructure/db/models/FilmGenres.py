from sqlalchemy import Column, Integer, ForeignKey, Table
from Base import Base

film_genres = Table(
    'film_genres',
    Base.metadata,
    Column('id_genre', Integer, ForeignKey('genres.id'), primary_key=True),
    Column('id_film', Integer, ForeignKey('films.id'), primary_key=True)
)