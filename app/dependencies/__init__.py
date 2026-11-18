from .pagination import PaginationDep
from .repos import (
    AuthorOr404Dep,
    AuthorRepositoryDep,
    BookOr404Dep,
    BookRepositoryDep,
    GenreOr404Dep,
    GenreRepositoryDep,
)

__all__ = (
    "AuthorOr404Dep",
    "AuthorRepositoryDep",
    "BookOr404Dep",
    "BookRepositoryDep",
    "GenreOr404Dep",
    "GenreRepositoryDep",
    "PaginationDep"
)
