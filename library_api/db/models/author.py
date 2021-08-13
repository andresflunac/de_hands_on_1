import datetime

from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship
from library_api.db.models.book import Book
from library_api.db.session import Base


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    birthdate = Column(Date)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())

    books = relationship("Book", order_by=Book.id, back_populates="author")

    def __init__(self, first_name, last_name, birthdate):
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
