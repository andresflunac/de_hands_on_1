import datetime
import pytest

from typing import List, Generator, Dict
from fastapi.testclient import TestClient
from requests import Response
# run_around_test is required as test listener
from tests.api.routers.utils import override_get_db_session, test_session, run_around_each_test
from library_api.db.models.author import Author
from library_api.main import app
from library_api.api.dependencies import get_db_session

app.dependency_overrides[get_db_session] = override_get_db_session

test_client: TestClient = TestClient(app)


@pytest.mark.it('List all authors')
def test_list_all_authors():
    db: Generator = test_session()
    authors: List[Author] = [
        Author(first_name="firstname1", last_name="lastname1", birthdate=datetime.date.today()),
        Author(first_name="firstname2", last_name="lastname2", birthdate=datetime.date.today()),
        Author(first_name="firstname3", last_name="lastname3", birthdate=datetime.date.today())
    ]
    db.add_all(authors)
    db.commit()

    response: Response = test_client.get("/authors/")
    all_authors: List[dict] = response.json()

    assert response.status_code == 200
    assert len(all_authors) == 3
    for author in all_authors:
        assert set(author.keys()) == {"id", "first_name", "last_name", "birthdate"}


@pytest.mark.it('Create a new author')
def test_create_author():
    db = test_session()
    author = {"first_name": "fn", "last_name": "ln",
              "birthdate": datetime.date.today().isoformat()}

    response = test_client.post("/authors/", json=author)
    author_in_response = response.json()
    author_in_db: Author = db.query(Author).filter(Author.id == author_in_response["id"]).one()

    assert response.status_code == 200
    assert author_in_db.first_name == author["first_name"]
    assert author_in_db.last_name == author["last_name"]
    assert author_in_db.birthdate.isoformat() == author["birthdate"]


@pytest.mark.it('Update an author')
def test_update_author():
    db: Generator = test_session()
    author: Author = Author(
        first_name="firstname1",
        last_name="lastname1",
        birthdate=datetime.date.fromisoformat("2021-01-01")
    )
    db.add(author)
    db.commit()

    author_id: int = author.id

    new_author_data: Dict[str, str, datetime.date] = {
        "first_name": "firstname2",
        "last_name": "lastname2",
        "birthdate": datetime.date.today().isoformat()
    }

    response = test_client.put(f"/authors/{author_id}", json=new_author_data)
    author_in_response = response.json()
    db.refresh(author)

    assert response.status_code == 200
    # Object in db was updated
    assert author.first_name == new_author_data["first_name"]
    assert author.last_name == new_author_data["last_name"]
    assert author.birthdate.isoformat() == new_author_data["birthdate"]
    # Response data is the new data
    assert author_in_response["first_name"] == new_author_data["first_name"]
    assert author_in_response["last_name"] == new_author_data["last_name"]
    assert author_in_response["birthdate"] == new_author_data["birthdate"]


@pytest.mark.it('Throw when author id does not exists')
def test_update_non_existing_author():
    new_author_data: Dict[str, str, datetime.date] = {
        "first_name": "firstname2",
        "last_name": "lastname2",
        "birthdate": datetime.date.today().isoformat()
    }

    response = test_client.put("/authors/999", json=new_author_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Author not found"
