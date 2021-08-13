import datetime
from typing import List

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException

from library_api.api.schemata.author import Author, AuthorBase
from library_api.db.models.author import Author as AuthorInDb
from library_api.api.dependencies import get_db_session

router = APIRouter()


@router.get("/", response_model=List[Author])
async def get_all_authors(session=Depends(get_db_session)):
    return session.query(AuthorInDb).all()


@router.post("/", response_model=Author)
async def create_author(*, session=Depends(get_db_session), author: AuthorBase):
    current_time = datetime.datetime.now()
    author_data = author.dict()
    author_in_db = AuthorInDb(**author_data, created_at=current_time, updated_at=current_time)
    session.add(author_in_db)
    session.commit()

    return author_in_db


# Refactor such that all data is not required
@router.put("/{author_id}", response_model=Author)
async def update_author(*, author_id: int, author: AuthorBase, session=Depends(get_db_session)):
    try:
        author_in_db: AuthorInDb = session.query(AuthorInDb).filter(AuthorInDb.id == author_id).one()
    except sqlalchemy.orm.exc.NoResultFound:
        author_in_db = None

    if not author_in_db:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    author_in_db.first_name = author.first_name
    author_in_db.last_name = author.last_name
    author_in_db.birthdate = author.birthdate
    session.commit()

    return author_in_db
