from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from typing import List, Optional

from app.domain.models.Film import Film
from app.infrastructure.db.models.FilmORM import FilmORM


class FilmRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_film(self, film: Film) -> Film:
        film_orm = FilmORM(
            title=film.title,
            description=film.description,
            creation_date=film.creation_date,
            file_link=film.file_link
        )

        self.session.add(film_orm)

        await self.session.commit()
        await self.session.refresh(film_orm)

        return Film(
            id=film_orm.id,
            title=film_orm.title,
            description=film_orm.description,
            creation_date=film_orm.creation_date,
            file_link=film_orm.file_link
        )

    async def get_film_by_id(self, film_id: int) -> Optional[Film]:
        result = await self.session.execute(select(FilmORM).filter_by(id=film_id))
        film_orm = result.scalar_one_or_none()
        if film_orm:
            return Film(
                id=film_orm.id,
                title=film_orm.title,
                description=film_orm.description,
                creation_date=film_orm.creation_date,
                file_link=film_orm.file_link
            )
        return None

    async def get_all_films(self) -> List[Film]:
        result = await self.session.execute(select(FilmORM))
        films = result.scalars().all()
        return [Film(
            id=f.id,
            title=f.title,
            description=f.description,
            creation_date=f.creation_date,
            file_link=f.file_link
        ) for f in films]