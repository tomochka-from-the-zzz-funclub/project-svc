from datetime import date
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.Film import Film
from app.domain.models.Genre import Genre

from app.domain.repositories.FilmRepository import FilmRepository
from app.domain.repositories.GenreRepository import GenreRepository

from app.infrastructure.db.models.FilmORM import FilmORM
from app.infrastructure.db.models.GenreORM import GenreORM


class FilmService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.film_repository = FilmRepository(session)
        self.genre_repository = GenreRepository(session)

    async def add_film_with_genres(self, film: Film, genre_ids: List[int]) -> Film:
        """
        Создание фильма с привязкой к жанрам.

        :param film: Объект Film, содержащий данные о фильме.
        :param genre_ids: Список ID жанров для привязки к фильму.
        :return: Объект Film с привязанными жанрами.
        """

        film_orm = await self.film_repository.add_film(film)

        genres = await self.genre_repository.get_genres_by_ids(genre_ids)

        film_orm = await self.assign_genres_to_film(film_orm, genres)

        return Film(
            id=film_orm.id,
            title=film_orm.title,
            description=film_orm.description,
            creation_date=film_orm.creation_date,
            file_link=film_orm.file_link,
            genres=[Genre(id=g.id, name=g.name) for g in film_orm.genres],
        )

    async def assign_genres_to_film(self, film_orm: FilmORM, genres: List[GenreORM]) -> FilmORM:
        """
        Присваивает жанры фильму.

        :param film_orm: Объект ORM фильма, к которому нужно привязать жанры.
        :param genres: Список объектов ORM жанров.
        :return: Обновленный объект ORM фильма.
        """
        for genre in genres:
            film_orm.genres.append(genre)

        await self.session.commit()
        await self.session.refresh(film_orm)

        return film_orm