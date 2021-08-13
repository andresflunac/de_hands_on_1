from fastapi import FastAPI
from library_api.api.api import api_router
from library_api.db.session import Base, engine, db_session
from .db.models.author import Author
from .db.models.genre import Genre
from .db.models.book import Book
import datetime


app = FastAPI()

app.include_router(api_router)

# drop and create all tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# mock data
author1 = Author('Rachel', 'Yoder', datetime.date(1930, 11, 30))
author2 = Author('Amy', 'Harmon', datetime.date(1960, 6, 11))
author3 = Author('Daniel', 'Silva', datetime.date(1970, 4, 23))
author4 = Author('Trevor', 'Noah', datetime.date(1965, 8, 9))
author5 = Author('Douglas', 'Adams', datetime.date(1967, 2, 10))
author6 = Author('Stephen', 'King', datetime.date(1878, 11, 20))
genre1 = Genre('Action', 'An action story is similar to adventure, and the protagonist usually takes a risky turn, which leads to desperate situations ...')
genre2 = Genre('Comedy', 'is a story that tells about a series of funny, or comical events, intended to make the audience laugh')
genre3 = Genre('Fantasy', 'A fantasy story is about magic or supernatural forces, as opposed to technology as seen in science fiction.')
genre4 = Genre('Horror', 'A horror story is told to deliberately scare or frighten the audience, through suspense, violence or shock')
genre5 = Genre('Romance', 'The term romance has multiple meanings; for example, historical romances like those of Walter Scott would use the term to mean a...')
book1 = Book('Nightbitch', 1, 1)
book2 = Book('The Second Blind Son', 1, 2)
book3 = Book('Born a Crime', 2, 4)
book4 = Book('House of Leaves', 4, 4)
book5 = Book('Beach Read', 5, 5)
book6 = Book('The Cellist (Gabriel Allon, #21)', 1, 3)
book7 = Book('Alicia', 1, 1)
book8 = Book('Mexican Gothic', 3, 4)
book9 = Book('The Ultimate Hitchhikers Guide ', 2, 4)
book10 = Book('Outlander', 5, 2)
book11 = Book('Dracula', 4, 5)
book12 = Book('The Shining', 4, 5)
book13 = Book('Frankenstein', 3, 3)
book14 = Book('The Turn of the Screw', 2, 2)
book15 = Book('Jane Eyre', 5, 1)
inserts_authors = [author1, author2, author3, author4, author5, author6]
inserts_genres = [genre1, genre2, genre3, genre4, genre5]
inserts_books = [book1, book2, book3, book4, book5, book6, book7, book8, book9, book10, book11, book12, book13, book14, book15]

# feed tables
session = db_session()
session.add_all(inserts_authors)
session.add_all(inserts_genres)
session.add_all(inserts_books)
session.commit()
