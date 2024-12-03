from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.Film import Film
from app.domain.models.Genre import Genre
from app.domain.repositories.FilmGenresRepository import FilmGenresRepository
from app.domain.repositories.FilmRepository import FilmRepository
from app.domain.repositories.GenreRepository import GenreRepository
from app.infrastructure.db.models.FilmORM import FilmORM


class FilmService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.film_repository = FilmRepository(session)
        self.genre_repository = GenreRepository(session)
        self.film_genres_repository = FilmGenresRepository(session)

    async def create_film(self, film: Film, genres_name: List[str] = None) -> int:
        """
        Создание фильма с привязкой к жанрам.

        :param genres_name: Список названий жанров.
        :param film: Объект Film, содержащий данные о фильме.
        :return: Объект Film с привязанными жанрами.
        """

        film_id = await self.film_repository.add_film(film)

        for name in genres_name:
            genre_orm = await self.genre_repository.get_genre_by_name(name)

            await self.film_genres_repository.add_genre_to_film(film_id, genre_orm.id)

        return film_id

    async def add_genres_to_film(self, film_name: str, genres_name: List[str]) -> None:
        """
        :param film_name: Навзание фильма
        :param genres_name: Список названий жанров

        """
        film_orm = await self.film_repository.get_film_by_title(film_name)

        for name in genres_name:
            genre_orm = await self.genre_repository.get_genre_by_name(name)
            await self.film_genres_repository.add_genre_to_film(film_orm.id, genre_orm.id)

    async def delete_genres_from_film(self, film_name: str, genres_name: List[str]) -> None:
        """
        :param film_name: Навзание фильма
        :param genres_name: Список названий жанров

        """
        film_orm = await self.film_repository.get_film_by_title(film_name)

        for name in genres_name:
            genre_orm = await self.genre_repository.get_genre_by_name(name)
            await self.film_genres_repository.remove_genre_from_film(film_orm.id, genre_orm.id)


    async def get_all_films(self) -> List[Film]:
        """
        Получает все фильмы из базы данных.
        :return: Список объектов FilmORM.
        """
        films_orm = await self.film_repository.get_all_films()
        films = [Film(id=f.id, title=f.title, description=f.description, creation_date=f.creation_date, file_link=f.file_link) for f in films_orm]

        return films

    async def get_film_data(self, film_name: str) -> Film:
        """
        Получение фильма с его жанрами.

        :param film_name: Название фильма.
        :return: Объект Film с жанрами.
        """
        film_orm = await self.film_repository.get_film_by_title(film_name)
        genres = [Genre(id=g.id, name=g.name) for g in film_orm.genres]

        return Film(
            id=film_orm.id,
            title=film_orm.title,
            description=film_orm.description,
            creation_date=film_orm.creation_date,
            file_link=film_orm.file_link,
            genres=genres,
        )

    async def get_films_by_genre_name(self, genre_name: str) -> List[Film]:
        """
        Получение фильмов по жанру.

        :param genre_name: Название жанра.
        :return: Объект Film с жанрами.
        """
        genre_orm = await self.genre_repository.get_genre_by_name(genre_name)
        films_orm = await self.film_genres_repository.get_films_by_genre_id(genre_orm.id)
        films = [Film(id=f.id, title=f.title, description=f.description, creation_date=f.creation_date, file_link=f.file_link) for f in films_orm]

        return films

    async def update_film(self, film_name: str, updated_film: Film) -> Film:
        """
        Обновление информации о фильме.

        :param film_name: Название фильма.
        :param updated_film: Объект Film с новыми данными.
        :return: Обновленный объект Film.
        """

        film_orm = await self.film_repository.get_film_by_title(film_name)
        updated_film_orm = await self.film_repository.update_film(film_orm.id, updated_film)

        return Film(
            id=updated_film_orm.id,
            title=updated_film_orm.title,
            description=updated_film_orm.description,
            creation_date=updated_film_orm.creation_date,
            file_link=updated_film_orm.file_link,
            genres=[Genre(id=g.id, name=g.name) for g in updated_film_orm.genres],
        )

    async def delete_film(self, film_name: str) -> None:
        """
        Удаление фильма по ID.

        :param film_name: Название фильма для удаления.
        """
        film_orm = await self.film_repository.get_film_by_title(film_name)
        await self.film_repository.delete_film(film_orm.id)
