from typing import Generator, List

import pytest

from requests import Response
from fastapi.testclient import TestClient
# run_around_test is required as test listener
from tests.api.routers.utils import override_get_db_session, test_session, run_around_each_test
from library_api.api.dependencies import get_db_session
from library_api.db.models.genre import Genre
from library_api.main import app

app.dependency_overrides[get_db_session] = override_get_db_session

test_client: TestClient = TestClient(app)


@pytest.mark.it("List all genre")
def test_list_all_genre():
    db: Generator = test_session()
    genres: List[Genre] = [
        Genre(name="Horror", description="scary"),
        Genre(name="Romantic", description="love")
    ]
    db.add_all(genres)
    db.commit()

    response: Response = test_client.get("/genres/")

    assert response.status_code == 200
    assert len(response.json()) == 2
