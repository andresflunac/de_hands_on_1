import datetime

from pydantic import BaseModel


class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    birthdate: datetime.date

    class Config:
        arbitrary_types_allowed = True


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True
