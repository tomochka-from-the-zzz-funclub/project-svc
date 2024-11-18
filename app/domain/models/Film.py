from dataclasses import dataclass
from datetime import date
from typing import Optional

from app.domain.models.Genre import Genre


@dataclass
class Film:
    id: Optional[int] = None
    title: str = ""
    description: Optional[str] = None
    creation_date: Optional[date] = None
    file_link: Optional[str] = None
    genres: Optional[list[Genre]] = None

    def __repr__(self) -> str:
        """
        Форматированный вывод для отладки.
        """
        genres = ", ".join(genre.name for genre in self.genres) if self.genres else "None"
        return (
            f"<Film ID={self.id}, Title='{self.title}', "
            f"Description='{self.description or 'None'}', "
            f"CreationDate='{self.creation_date or 'None'}', "
            f"FileLink='{self.file_link or 'None'}', Genres=[{genres}]>"
        )

    def __str__(self) -> str:
        """
        Упрощённый вывод для отображения в пользовательском интерфейсе.
        """
        genres = ", ".join(genre.name for genre in self.genres) if self.genres else "Нет жанров"
        return (
            f"Фильм: {self.title}\n"
            f"Описание: {self.description or 'Нет описания'}\n"
            f"Дата выпуска: {self.creation_date or 'Не указана'}\n"
            f"Ссылка: {self.file_link or 'Нет ссылки'}\n"
            f"Жанры: {genres}"
        )

