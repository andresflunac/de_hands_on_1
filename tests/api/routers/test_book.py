import datetime
from typing import Generator, List

import pytest

from library_api.main import app
from fastapi.testclient import TestClient
from tests.api.routers.utils import test_session, override_get_db_session, run_around_each_test
from library_api.api.dependencies import get_db_session
from library_api.db.models.author import Author
from library_api.db.models.book import Book
from library_api.db.models.genre import Genre

app.dependency_overrides[get_db_session] = override_get_db_session

test_client: TestClient = TestClient(app)


@pytest.mark.it("List all books")
def test_list_all_books():
    db: Generator = test_session()
    authors: List[Author] = [
        Author(first_name="firstname1", last_name="lastname1", birthdate=datetime.date.today()),
        Author(first_name="firstname2", last_name="lastname2", birthdate=datetime.date.today())
    ]
    db.add_all(authors)
    genres: List[Genre] = [
        Genre(name="genre1", description="desc1"),
        Genre(name="genre2", description="desc2")
    ]
    db.add_all(genres)
    books: List[Book] = [
        Book(name="book1", genre_id=1, author_id=1),
        Book(name="book2", genre_id=2, author_id=2)
    ]
    db.add_all(books)
    db.commit()

    response = test_client.get("/books/")

    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.it("List all books filtered by author_id")
def test_list_all_books_filter_author_id():
    db: Generator = test_session()
    authors: List[Author] = [
        Author(first_name="firstname1", last_name="lastname1", birthdate=datetime.date.today()),
        Author(first_name="firstname2", last_name="lastname2", birthdate=datetime.date.today())
    ]
    db.add_all(authors)
    genres: List[Genre] = [
        Genre(name="genre1", description="desc1"),
        Genre(name="genre2", description="desc2")
    ]
    db.add_all(genres)
    books: List[Book] = [
        Book(name="book1", genre_id=1, author_id=1),
        Book(name="book2", genre_id=2, author_id=2)
    ]
    db.add_all(books)
    db.commit()

    response = test_client.get("/books/?author_id=1")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.it("List all books filtered by genre_id")
def test_list_all_books_filter_genre_id():
    db: Generator = test_session()
    authors: List[Author] = [
        Author(first_name="firstname1", last_name="lastname1", birthdate=datetime.date.today()),
        Author(first_name="firstname2", last_name="lastname2", birthdate=datetime.date.today())
    ]
    db.add_all(authors)
    genres: List[Genre] = [
        Genre(name="genre1", description="desc1"),
        Genre(name="genre2", description="desc2")
    ]
    db.add_all(genres)
    books: List[Book] = [
        Book(name="book1", genre_id=1, author_id=1),
        Book(name="book2", genre_id=2, author_id=2)
    ]
    db.add_all(books)
    db.commit()

    response = test_client.get("/books/?genre_id=1")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.it("List all books filtered by author_id and genre_id")
def test_list_all_books_filter_author_genre_id():
    db: Generator = test_session()
    authors: List[Author] = [
        Author(first_name="firstname1", last_name="lastname1", birthdate=datetime.date.today()),
        Author(first_name="firstname2", last_name="lastname2", birthdate=datetime.date.today())
    ]
    db.add_all(authors)
    genres: List[Genre] = [
        Genre(name="genre1", description="desc1"),
        Genre(name="genre2", description="desc2")
    ]
    db.add_all(genres)
    books: List[Book] = [
        Book(name="book1", genre_id=1, author_id=1),
        Book(name="book2", genre_id=2, author_id=2)
    ]
    db.add_all(books)
    db.commit()

    response = test_client.get("/books/?author_id=1&genre_id=2")

    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.it("Create a book")
def test_create_a_book():
    db: Generator = test_session()
    author: Author = Author(first_name="firstname1", last_name="lastname1", birthdate=datetime.date.today())
    db.add(author)
    genre: Genre = Genre(name="genre1", description="desc1")
    db.add(genre)
    db.commit()
    book_data = {"name": "book1", "genre_id": 1, "author_id": 1}

    response = test_client.post("/books/", json=book_data)
    book_in_response = response.json()

    assert response.status_code == 200
    assert book_in_response["name"] == book_data["name"]
    assert book_in_response["genre_id"] == book_data["genre_id"]
    assert book_in_response["author_id"] == book_data["author_id"]


@pytest.mark.it("Update a book")
def test_update_a_book():
    current_time = datetime.datetime.now()
    db: Generator = test_session()
    authors: List[Author] = [
        Author(first_name="firstname1", last_name="lastname1", birthdate=datetime.date.today()),
        Author(first_name="firstname2", last_name="lastname2", birthdate=datetime.date.today())
    ]
    db.add_all(authors)
    genres: List[Genre] = [
        Genre(name="genre1", description="desc1"),
        Genre(name="genre2", description="desc2")
    ]
    db.add_all(genres)
    book = Book(
        name="book1", genre_id=1, author_id=1,
        created_at=current_time, updated_at=current_time)

    db.add(book)
    db.commit()

    book_id = book.id

    new_book_data = {"name": "the new name", "author_id": 2}

    response = test_client.put(f"/books/{book_id}", json=new_book_data)
    book_in_response = response.json()

    db.refresh(book)

    assert response.status_code == 200
    # Book updated on DB
    assert book.name == "the new name"
    assert book.author_id == 2
    assert book.genre_id == 1
    assert book.created_at == current_time
    assert book.updated_at > current_time
    # Book in response matches new book data
    assert book.name == book_in_response["name"]
    assert book.author_id == book_in_response["author_id"]
    assert book.genre_id == book_in_response["genre_id"]


@pytest.mark.it("Delete a book")
def test_delete_a_book():
    db: Generator = test_session()
    author: Author = Author(first_name="firstname1", last_name="lastname1", birthdate=datetime.date.today())
    db.add(author)
    genre: Genre = Genre(name="genre1", description="desc1")
    db.add(genre)
    book = Book(name="book1", genre_id=1, author_id=1)
    db.add(book)
    db.commit()

    book_id = book.id

    response = test_client.delete(f"/books/{book_id}")

    delete_response = response.json()

    query_result = db.query(Book).filter(Book.id == book_id).all()

    assert response.status_code == 200
    assert delete_response["id"] == book_id
    assert delete_response["action"] == "deleted"
    assert len(query_result) == 0

