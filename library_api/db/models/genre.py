import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from library_api.db.models.book import Book
from library_api.db.session import Base


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())

    books = relationship("Book", order_by=Book.id, back_populates="genre")

    def __init__(self, name, description):
        self.name = name
        self.description = description