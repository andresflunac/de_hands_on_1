from typing import List

from fastapi import APIRouter, Depends

from library_api.api.dependencies import get_db_session
from library_api.api.schemata.genre import Genre
from library_api.db.models.genre import Genre as GenreInDb

router = APIRouter()


@router.get("/", response_model=List[Genre])
async def list_all_genres(session=Depends(get_db_session)):
    return session.query(GenreInDb).all()
