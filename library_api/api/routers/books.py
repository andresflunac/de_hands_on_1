import datetime
from typing import List, Optional

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_

from library_api.api.dependencies import get_db_session
from library_api.api.schemata.book import Book, BookBase, BookUpdate
from library_api.db.models.book import Book as BookInDb

router = APIRouter()


@router.get("/", response_model=List[Book])
async def list_all_books(
        session=Depends(get_db_session),
        author_id: Optional[int] = None,
        genre_id: Optional[int] = None
):
    if author_id and genre_id:
        return session.query(BookInDb) \
            .filter(
            and_(
                BookInDb.author_id == author_id,
                BookInDb.genre_id == genre_id
            )).all()
    elif author_id:
        return session.query(BookInDb) \
            .filter(BookInDb.author_id == author_id).all()
    elif genre_id:
        return session.query(BookInDb) \
            .filter(BookInDb.genre_id == genre_id).all()
    else:
        return session.query(BookInDb).all()


@router.post("/", response_model=Book)
async def create_book(*, session=Depends(get_db_session), book: BookBase):
    current_time = datetime.datetime.now()
    book_data = book.dict()
    book_in_db = BookInDb(**book_data, created_at=current_time, updated_at=current_time)
    session.add(book_in_db)
    session.commit()

    return book_in_db


@router.put("/{book_id}", response_model=Book)
async def update_book(
        *, session=Depends(get_db_session),
        book_id: int, new_book_data: BookUpdate):
    current_time = datetime.datetime.now()

    try:
        book_in_db: BookInDb = session.query(BookInDb).filter(BookInDb.id == book_id).one()
    except sqlalchemy.orm.exc.NoResultFound:
        book_in_db = None

    if not book_in_db:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    for field in new_book_data.dict(exclude_unset=True).keys():
        setattr(book_in_db, field, new_book_data.__getattribute__(field))

    book_in_db.updated_at = current_time

    session.commit()

    return book_in_db


@router.delete("/{book_id}")
async def delete_book(*, session=Depends(get_db_session), book_id : int):
    try:
        book_in_db: BookInDb = session.query(BookInDb).filter(BookInDb.id == book_id).one()
    except sqlalchemy.orm.exc.NoResultFound:
        book_in_db = None

    if not book_in_db:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    session.delete(book_in_db)
    session.commit()

    return {"id": book_id, "action": "deleted"}
