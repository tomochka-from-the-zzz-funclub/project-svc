from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import delete, insert

from app.infrastructure.db.models.Base import Base
from app.infrastructure.db.models.FilmORM import FilmORM
from app.infrastructure.db.models.GenreORM import GenreORM
from app.infrastructure.db.models.FilmGenres import film_genres


class FilmGenresRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_genre_to_film(self, film_id: int, genre_id: int) -> None:
        """
        Добавляет связь между фильмом и жанром.

        :param film_id: ID фильма.
        :param genre_id: ID жанра.
        """
        query = insert(film_genres).values(id_film=film_id, id_genre=genre_id)
        await self.session.execute(query)
        await self.session.commit()

    async def remove_genre_from_film(self, film_id: int, genre_id: int) -> None:
        """
        Удаляет связь между фильмом и жанром.

        :param film_id: ID фильма.
        :param genre_id: ID жанра.
        """
        query = delete(film_genres).where(
            (film_genres.c.id_film == film_id) & (film_genres.c.id_genre == genre_id)
        )
        await self.session.execute(query)
        await self.session.commit()

    async def get_genres_by_film_id(self, film_id: int) -> List[GenreORM]:
        """
        Получает все жанры, связанные с фильмом.

        :param film_id: ID фильма.
        :return: Список объектов GenreORM.
        """
        query = (
            select(GenreORM)
            .join(film_genres, film_genres.c.id_genre == GenreORM.id)
            .where(film_genres.c.id_film == film_id)
        )
        result = await self.session.execute(query)
        genres = list(result.scalars().all())
        return genres

    async def get_films_by_genre_id(self, genre_id: int) -> List[FilmORM]:
        """
        Получает все фильмы, связанные с жанром.

        :param genre_id: ID жанра.
        :return: Список объектов FilmORM.
        """
        query = (
            select(FilmORM)
            .join(film_genres, film_genres.c.id_film == FilmORM.id)
            .where(film_genres.c.id_genre == genre_id)
        )
        result = await self.session.execute(query)
        films = list(result.scalars().all())
        return films
