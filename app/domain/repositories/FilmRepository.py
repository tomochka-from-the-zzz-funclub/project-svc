from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.domain.models.Film import Film
from app.infrastructure.db.models.FilmORM import FilmORM


class FilmRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_film(self, film: Film) -> Film:
        """
        Создание нового фильма в базе данных.

        :param film: Объект Film, содержащий данные о фильме.
        :return: Объект Film, представляющий созданный фильм.
        """
        try:
            existing_film = await self.get_film_by_title(film.title)
            if existing_film:
                return existing_film

            film_orm = FilmORM(
                title=film.title,
                description=film.description,
                creation_date=film.creation_date,
                file_link=film.file_link,
            )

            self.session.add(film_orm)
            await self.session.commit()
            await self.session.refresh(film_orm)

            return Film(
                id=film_orm.id,
                title=film_orm.title,
                description=film_orm.description,
                creation_date=film_orm.creation_date,
                file_link=film_orm.file_link,
            )

        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Не удалось добавить жанр из-за конфликта данных.")


    async def get_film_by_id(self, film_id: int) -> Optional[Film]:
        """
        Получает фильм по ID.

        :param film_id: ID фильма, который нужно найти
        :return: Объект Film
        :raises ValueError: Если фильм с указанным названием не найден.
        """
        result = await self.session.execute(select(FilmORM).filter_by(id=film_id))
        film_orm = result.scalars().first()

        if film_orm:
            return Film(
                id=film_orm.id,
                title=film_orm.title,
                description=film_orm.description,
                creation_date=film_orm.creation_date,
                file_link=film_orm.file_link
            )

        raise ValueError(
            f"Фильм с названием '{film_id}' не найден. Проверьте правильность названия или добавьте новый фильм."
        )

    async def get_films_by_ids(self, film_ids: List[int]) -> List[Film]:
        """
        Получает фильмы по их ID, используя метод get_film_by_id.

        :param film_ids: List[int] — Список ID фильмов.
        :return: List[Film] — Список объектов фильмов.
        """
        return [await self.get_film_by_id(film_id) for film_id in film_ids]


    async def get_all_films(self) -> List[Film]:
        """
        Получает все фильмы из базы данных.

        :return: Список объектов Film
        """
        result = await self.session.execute(select(FilmORM))
        films = result.scalars().all()

        return [Film(
            id=film.id,
            title=film.title,
            description=film.description,
            creation_date=film.creation_date,
            file_link=film.file_link
        ) for film in films]

    async def get_film_by_title(self, title: str) -> Film:
        """
        Получение фильма по названию.

        :param title: str — Название фильма.
        :return: Film — объект фильма, если найден.
        :raises ValueError: Если фильм с указанным названием не найден.
        """
        result = await self.session.execute(select(FilmORM).filter_by(title=title))
        film_orm = result.scalars().first()

        if not film_orm:
            return Film(
                id=film_orm.id,
                title=film_orm.title,
                description=film_orm.description,
                creation_date=film_orm.creation_date,
                file_link=film_orm.file_link
            )

        raise ValueError(
            f"Фильм с названием '{title}' не найден. Проверьте правильность названия или добавьте новый фильм."
        )

    async def update_film(self, film_id: int, updated_film: Film) -> Optional[Film]:
        """
        Обновляет данные о фильме.

        :param film_id: ID фильма, который нужно обновить
        :param updated_film: Обновленный объект Film
        :return: Обновленный объект Film, если фильм найден и обновлен, или None
        """
        film = await self.get_film_by_id(film_id)

        if film:
            film.title = updated_film.title
            film.description = updated_film.description
            film.creation_date = updated_film.creation_date
            film.file_link = updated_film.file_link

            await self.session.commit()

            return film

        return None

    async def delete_film(self, film_id: int) -> Optional[Film]:
        """
        Удаляет фильм по ID.

        :param film_id: ID фильма, который нужно удалить
        :return: Удаленный объект Film, если фильм найден и удален, или None
        """
        film = await self.get_film_by_id(film_id)

        if film:
            await self.session.delete(film)
            await self.session.commit()

            return film

        return None
