from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.domain.models.Genre import Genre
from app.infrastructure.db.models.GenreORM import GenreORM


class GenreRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_genre(self, genre: Genre) -> Genre:
        """
        Добавление нового жанра в базу данных, если он еще не существует.

        :param genre: Genre — объект жанра для добавления.
        :return: Genre — объект жанра с присвоенным ID (существующий или новый).
        """
        try:
            existing_genre = await self.get_genre_by_name(genre.name)
            if existing_genre:
                return existing_genre

            genre_orm = GenreORM(name=genre.name)
            self.session.add(genre_orm)

            await self.session.commit()
            await self.session.refresh(genre_orm)

            return Genre(id=genre_orm.id, name=genre_orm.name)

        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Не удалось добавить жанр из-за конфликта данных.")

    async def get_genre_by_id(self, genre_id: int) -> Optional[Genre]:
        """
        Получение жанра по ID.

        :param genre_id: int — ID жанра.
        :return: Genre или None — объект жанра, если найден, иначе None.
        :raises ValueError: Если жанр с указанным ID не найден.
        """
        result = await self.session.execute(select(GenreORM).filter_by(id=genre_id))
        genre_orm = result.scalars().first()

        if genre_orm:
            return Genre(id=genre_orm.id, name=genre_orm.name)

        raise ValueError(
            f"Жанр с ID {genre_id} не найден в базе данных. "
            f"Убедитесь, что вы указали корректный ID жанра. "
            f"Если жанр отсутствует, его нужно создать перед использованием."
        )

    async def get_genres_by_ids(self, genre_ids: List[int]) -> List[Genre]:
        """
        Получает жанры по их ID, используя метод get_genre_by_id.

        :param genre_ids: Список ID жанров.
        :return: Список объектов Genre.
        """
        return [await self.get_genre_by_id(genre_id) for genre_id in genre_ids]

    async def get_genre_by_name(self, name: str) -> Optional[Genre]:
        """
        Получение жанра по названию.

        :param name: str — Название жанра.
        :return: Genre или None — объект жанра, если найден, или None.
        """
        result = await self.session.execute(select(GenreORM).filter_by(name=name))
        genre_orm = result.scalars().first()

        if genre_orm:
            return Genre(id=genre_orm.id, name=genre_orm.name)

        return None

    async def get_all_genres(self) -> List[Genre]:
        """
        Получение всех жанров.

        :return: List[Genre] — список объектов жанров.
        """
        result = await self.session.execute(select(GenreORM))
        genres_orm = result.scalars().all()

        return [Genre(id=genre.id, name=genre.name) for genre in genres_orm]

    async def update_genre(self, genre_id: int, updated_genre: Genre) -> Optional[Genre]:
        """
        Обновление информации о жанре по ID.

        :param genre_id: int — ID жанра для обновления.
        :param updated_genre: Genre — новый объект жанра.
        :return: Genre или None — обновлённый объект жанра или None, если не найден.
        """
        genre = await self.get_genre_by_id(genre_id)

        if genre:
            genre.name = updated_genre.name

            await self.session.commit()

            return genre

        return None

    async def delete_genre(self, genre_id: int) -> Optional[Genre]:
        """
        Удаление жанра по ID.

        :param genre_id: int — ID жанра для удаления.
        :return: Genre или None — удалённый объект жанра или None, если не найден.
        """
        genre = await self.get_genre_by_id(genre_id)

        if genre:
            await self.session.delete(genre)
            await self.session.commit()

            return genre

        return None
