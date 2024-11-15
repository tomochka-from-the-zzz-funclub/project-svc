from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Film:
    id: Optional[int] = None
    title: str = ""
    description: Optional[str] = None
    creation_date: Optional[date] = None
    file_link: Optional[str] = None