from typing import List

from app.domain.models.Film import Film
from app.domain.models.Genre import Genre
from app.domain.repositories.FilmRepository import FilmRepository
from app.domain.repositories.GenreRepository import GenreRepository
from app.infrastructure.db.models.FilmORM import FilmORM
from app.infrastructure.db.models.GenreORM import GenreORM


class FilmService:
    def __init__(self, film_repo: FilmRepository, genre_repo: GenreRepository):
        self.film_repo = film_repo
        self.genre_repo = genre_repo

    async def create_film(self, title: str, description: str, creation_date, file_link: str) -> Film:
        film = Film(
            title=title,
            description=description,
            creation_date=creation_date,
            file_link=file_link
        )
        return await self.film_repo.add_film(film)

    async def get_all_films(self) -> List[Film]:
        return await self.film_repo.get_all_films()

    async def add_genre_to_film(self, film_id: int, genre_id: int):
        await self.validate_film_and_genre(film_id, genre_id)

        film_orm = await self.film_repo.session.get(FilmORM, film_id)
        genre_orm = await self.genre_repo.session.get(GenreORM, genre_id)
        film_orm.genres.append(genre_orm)
        await self.film_repo.session.commit()

    async def validate_film_and_genre(self, film_id, genre_id):
        film = await self.film_repo.get_film_by_id(film_id)
        genre = await self.genre_repo.get_genre_by_id(genre_id)
        if not film or not genre:
            raise ValueError("Film or Genre not found")

    async def get_all_genres(self) -> List[Genre]:
        return await self.genre_repo.get_all_genres()
