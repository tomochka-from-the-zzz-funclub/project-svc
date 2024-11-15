from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.domain.models.Genre import Genre
from app.infrastructure.db.models.GenreORM import GenreORM


class GenreRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_genre(self, genre: Genre) -> Genre:
        genre_orm = GenreORM(name=genre.name)
        self.session.add(genre_orm)
        await self.session.commit()
        await self.session.refresh(genre_orm)
        return Genre(id=genre_orm.id, name=genre_orm.name)

    async def get_genre_by_id(self, genre_id: int) -> Optional[Genre]:
        result = await self.session.execute(select(GenreORM).filter_by(id=genre_id))
        genre_orm = result.scalar_one_or_none()
        if genre_orm:
            return Genre(id=genre_orm.id, name=genre_orm.name)
        return None

    async def get_all_genres(self) -> List[Genre]:
        result = await self.session.execute(select(GenreORM))
        genres = result.scalars().all()
        return [Genre(id=g.id, name=g.name) for g in genres]