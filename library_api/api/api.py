from fastapi import APIRouter
from library_api.api.routers import authors, genres, books

api_router = APIRouter()

api_router.include_router(authors.router, prefix="/authors", tags=["authors"])
api_router.include_router(genres.router, prefix="/genres", tags=["genres"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
