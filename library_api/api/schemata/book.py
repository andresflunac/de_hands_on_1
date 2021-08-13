from typing import Optional

from pydantic import BaseModel

from library_api.api.schemata.author import Author
from library_api.api.schemata.genre import Genre


class BookUpdate(BaseModel):
    name: Optional[str] = None
    genre_id: Optional[int] = None
    author_id: Optional[int] = None


class BookBase(BaseModel):
    name: str
    genre_id: int
    author_id: int


class Book(BookBase):
    id: int
    author: Author
    genre: Genre

    class Config:
        orm_mode = True
