from dataclasses import dataclass
from typing import Optional

@dataclass
class Genre:
    id: Optional[int] = None
    name: str = ""

    def __repr__(self) -> str:
        """
        Форматированный вывод информации о жанре через repr.
        """
        return f"<Genre ID={self.id}, Name='{self.name}'>"

    def __str__(self) -> str:
        """
        Форматированный вывод информации о жанре.
        """
        return f"Жанр ID: {self.id}, Название: {self.name}"

