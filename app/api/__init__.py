from fastapi import APIRouter
from .authors import authors_router

main_router = APIRouter(prefix="/api")
main_router.include_router(authors_router)
