import asyncio

from app.domain.models.Genre import Genre
from app.infrastructure.db.CreateSession import AsyncSessionLocal
from app.domain.repositories.FilmRepository import FilmRepository
from app.domain.repositories.GenreRepository import GenreRepository
from app.use_cases.FilmService import FilmService
from app.infrastructure.db.models.FilmORM import FilmORM
from app.infrastructure.db.models.GenreORM import GenreORM


async def check_database_connection():
    async with AsyncSessionLocal() as session:
        try:
            # Проверяем подключение к базе данных
            if session.bind is None:
                print("Ошибка: Не удалось подключиться к базе данных")
                return

            print("Подключение к базе данных успешно установлено")

            # Создаем репозитории
            film_repo = FilmRepository(session)
            genre_repo = GenreRepository(session)

            # Создаем сервис для работы с фильмами и жанрами
            film_service = FilmService(film_repo, genre_repo)

            # Добавляем тестовые данные
            test_film_title = "Test Film"
            test_genre_name = Genre(name="Test Genre")

            # Создаем жанр
            genre = await genre_repo.add_genre(test_genre_name)
            print(f"Создан жанр: {genre.name}")

            # Создаем фильм
            film = await film_service.create_film(
                title=test_film_title,
                description="A test film description",
                creation_date="2024-01-01",
                file_link="http://example.com/test.mp4"
            )
            print(f"Создан фильм: {film.title}")


            # # Присваиваем жанр фильму
            # updated_film = await film_service.assign_genre_to_film(film_title=test_film_title,
            #                                                        genre_name=test_genre_name)
            # print(f"Жанр '{test_genre_name}' присвоен фильму '{test_film_title}'")
            #
            # # Проверяем получение всех фильмов
            # films = await film_repo.find_all()
            # print(f"Количество фильмов в базе: {len(films)}")
            #
            # # Удаляем тестовые данные, чтобы не оставлять следов
            # await session.delete(await session.get(FilmORM, film.id))
            # await session.delete(await session.get(GenreORM, genre.id))
            # await session.commit()
            # print("Тестовые данные успешно удалены")

        except Exception as e:
            print(f"Произошла ошибка: {e}")


