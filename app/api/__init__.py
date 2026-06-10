from fastapi import APIRouter
from .authors import authors_router
from .books import books_router

main_router = APIRouter(prefix="/api")
main_router.include_router(authors_router)
main_router.include_router(books_router)
