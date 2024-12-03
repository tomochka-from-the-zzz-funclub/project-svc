from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.Genre import Genre
from app.domain.repositories.GenreRepository import GenreRepository
from app.infrastructure.db.models.GenreORM import GenreORM


class GenreService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.genre_repository = GenreRepository(session)

    async def create_genre(self, genre: Genre) -> int:
        """
        Создание нового жанра в базе данных.

        :param genre: Объект Genre, содержащий данные о жанре.
        :return: ID созданного жанра.
        """
        genre_id = await self.genre_repository.add_genre(genre)
        return genre_id

    async def get_all_genres(self) -> List[Genre]:
        """
        Получает все жанры из базы данных.

        :return: Список объектов Genre.
        """
        genres_orm = await self.genre_repository.get_all_genres()
        genres = [Genre(id=g.id, name=g.name) for g in genres_orm]

        return genres

    async def get_genre_by_name(self, name: str) -> Genre:
        """
        Получает жанр по названию.

        :param name: Название жанра.
        :return: Объект Genre.
        """
        genre_orm = await self.genre_repository.get_genre_by_name(name)
        return Genre(id=genre_orm.id, name=genre_orm.name)

    async def update_genre(self, genre_name: str, updated_genre: Genre) -> Genre:
        """
        Обновляет информацию о жанре.

        :param genre_name: Название жанра для обновления.
        :param updated_genre: Обновленный объект Genre с новыми данными.
        :return: Обновленный объект Genre.
        """
        genre_orm = await self.genre_repository.get_genre_by_name(genre_name)
        updated_genre_orm = await self.genre_repository.update_genre(genre_orm.id, updated_genre)

        return Genre(id=updated_genre_orm.id, name=updated_genre_orm.name)

    async def delete_genre(self, genre_name: str) -> None:
        """
        Удаление жанра по названию.

        :param genre_name: Название жанра для удаления.
        """
        genre_orm = await self.genre_repository.get_genre_by_name(genre_name)
        await self.genre_repository.delete_genre(genre_orm.id)
