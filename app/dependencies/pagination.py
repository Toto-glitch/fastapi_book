from fastapi import Query
from typing import Annotated

from schemas import PaginationParams


def get_pagination_params(
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
) -> PaginationParams:
    return PaginationParams(page=page, limit=limit)
