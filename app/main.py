from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.MinioClient import get_video_from_s3
from starlette.responses import StreamingResponse

from app.domain.models.Film import Film
from app.domain.models.Genre import Genre
from app.infrastructure.db.CreateSession import get_session
from app.infrastructure.db.Settings import settings
from app.use_cases.FilmService import FilmService
from app.use_cases.GenreService import GenreService

app = FastAPI()

@app.post("/genres/", response_model=Genre)
async def create_genre(genre: Genre, session: AsyncSession = Depends(get_session)):
    genre_service = GenreService(session)
    genre_id = await genre_service.create_genre(genre)
    return Genre(id=genre_id, name=genre.name)

@app.get("/genres/", response_model=List[Genre])
async def get_all_genres(session: AsyncSession = Depends(get_session)):
    genre_service = GenreService(session)
    genres = await genre_service.get_all_genres()
    return genres

@app.get("/genres/{genre_name}", response_model=Genre)
async def get_genre_by_name(genre_name: str, session: AsyncSession = Depends(get_session)):
    genre_service = GenreService(session)
    genre = await genre_service.get_genre_by_name(genre_name)
    return genre

@app.put("/genres/{genre_name}", response_model=Genre)
async def update_genre(genre_name: str, updated_genre: Genre, session: AsyncSession = Depends(get_session)):
    genre_service = GenreService(session)
    updated = await genre_service.update_genre(genre_name, updated_genre)
    return updated

@app.delete("/genres/{genre_name}", status_code=204)
async def delete_genre(genre_name: str, session: AsyncSession = Depends(get_session)):
    genre_service = GenreService(session)
    await genre_service.delete_genre(genre_name)
    return {"message": "Genre deleted successfully"}

# Роуты для работы с фильмами

@app.post("/films/", response_model=int)
async def create_film(film: Film, genres_name: List[str], session: AsyncSession = Depends(get_session)):
    film_service = FilmService(session)
    film_id = await film_service.create_film(film, genres_name)
    return film_id

@app.get("/films/", response_model=List[Film])
async def get_all_films(session: AsyncSession = Depends(get_session)):
    film_service = FilmService(session)
    films = await film_service.get_all_films()
    return films

@app.get("/films/{film_name}", response_model=Film)
async def get_film_data(film_name: str, session: AsyncSession = Depends(get_session)):
    film_service = FilmService(session)
    film = await film_service.get_film_data(film_name)
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return film

@app.put("/films/{film_name}", response_model=Film)
async def update_film(film_name: str, updated_film: Film, session: AsyncSession = Depends(get_session)):
    film_service = FilmService(session)
    updated = await film_service.update_film(film_name, updated_film)
    return updated

@app.delete("/films/{film_name}", status_code=204)
async def delete_film(film_name: str, session: AsyncSession = Depends(get_session)):
    film_service = FilmService(session)
    await film_service.delete_film(film_name)
    return {"message": "Film deleted successfully"}

@app.post("/films/{film_name}/genres/")
async def add_genres_to_film(film_name: str, genres_name: List[str], session: AsyncSession = Depends(get_session)):
    film_service = FilmService(session)
    await film_service.add_genres_to_film(film_name, genres_name)
    return {"message": "Genres added successfully"}

@app.delete("/films/{film_name}/genres/")
async def remove_genres_from_film(film_name: str, genres_name: List[str], session: AsyncSession = Depends(get_session)):
    film_service = FilmService(session)
    await film_service.delete_genres_from_film(film_name, genres_name)
    return {"message": "Genres removed successfully"}

@app.get("/films/genre/{genre_name}", response_model=List[Film])
async def get_films_by_genre(genre_name: str, session: AsyncSession = Depends(get_session)):
    film_service = FilmService(session)
    films = await film_service.get_films_by_genre_name(genre_name)
    return films

@app.get("/video/{video_name}")
async def stream_video(video_name: str):
    """
    Стриминг видео из S3 хранилища.
    
    :param video_name: Имя файла видео в S3.
    :return: StreamingResponse для видео.
    """
    try:
        # Получаем видео с S3
        video_file = get_video_from_s3(settings.S3_BUCKET_NAME, video_name)
        
        # Стримим видео
        return StreamingResponse(video_file, media_type="video/mp4")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))