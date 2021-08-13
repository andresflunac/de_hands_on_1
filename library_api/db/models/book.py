import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from library_api.db.session import Base


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    genre_id = Column(Integer, ForeignKey("genre.id"))
    author_id = Column(Integer, ForeignKey("author.id"))
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())

    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="books")

    def __init__(self, name, genre_id, author_id):
        self.name = name
        self.genre_id = genre_id
        self.author_id = author_id