from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.infrastructure.db.models.GenreORM import GenreORM
from app.domain.models.Genre import Genre


class GenreRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_genre(self, genre: Genre) -> int:
        """
        Добавление нового жанра в базу данных, если он еще не существует.

        :param genre: Genre — объект жанра для добавления.
        :return: GenreORM — объект жанра с присвоенным ID.
        """
        try:
            existing_genre = await self.get_genre_by_name(genre.name)
            if existing_genre:
                return existing_genre.id

            genre_orm = GenreORM(name=genre.name)

            self.session.add(genre_orm)
            await self.session.commit()
            await self.session.refresh(genre_orm)

            return genre_orm.id

        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Не удалось добавить жанр из-за конфликта данных.")

    async def get_genre_by_id(self, genre_id: int) -> Optional[GenreORM]:
        """
        Получение жанра по ID.

        :param genre_id: int — ID жанра.
        :return: GenreORM или None — объект жанра, если найден, иначе None.
        """
        result = await self.session.execute(select(GenreORM).filter_by(id=genre_id))
        genre_orm = result.scalars().first()

        if genre_orm:
            return genre_orm

        return None

    async def get_genres_by_ids(self, genre_ids: List[int]) -> List[GenreORM]:
        """
        Получает жанры по их ID, используя метод get_genre_by_id.

        :param genre_ids: Список ID жанров.
        :return: Список объектов GenreORM.
        """
        return [await self.get_genre_by_id(genre_id) for genre_id in genre_ids]

    async def get_genre_by_name(self, name: str) -> Optional[GenreORM]:
        """
        Получение жанра по названию.

        :param name: str — Название жанра.
        :return: GenreORM или None — объект жанра, если найден, или None.
        """
        result = await self.session.execute(select(GenreORM).filter_by(name=name))
        genre_orm = result.scalars().first()

        if genre_orm:
            return genre_orm

        return None

    async def get_all_genres(self) -> List[GenreORM]:
        """
        Получение всех жанров.

        :return: List[GenreORM] — список объектов жанров.
        """
        result = await self.session.execute(select(GenreORM))
        genres_orm = list(result.scalars().all())

        return genres_orm

    async def update_genre(self, genre_id: int, updated_genre: Genre) -> Optional[GenreORM]:
        """
        Обновление информации о жанре по ID.

        :param genre_id: int — ID жанра для обновления.
        :param updated_genre: Genre — новый объект жанра.
        :return: GenreORM или None — обновлённый объект GenreORM или None, если не найден.
        """
        genre_orm = await self.get_genre_by_id(genre_id)

        if genre_orm:
            genre_orm.name = updated_genre.name
            await self.session.commit()

            return genre_orm

        return None

    async def delete_genre(self, genre_id: int) -> Optional[GenreORM]:
        """
        Удаление жанра по ID.

        :param genre_id: int — ID жанра для удаления.
        :return: GenreORM или None — удалённый объект GenreORM или None, если не найден.
        """
        genre_orm = await self.get_genre_by_id(genre_id)

        if genre_orm:
            await self.session.delete(genre_orm)
            await self.session.commit()

            return genre_orm

        return None
