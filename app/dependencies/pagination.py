from typing import Annotated

from fastapi import Depends
from schemas import PaginationParams

PaginationDep = Annotated[PaginationParams, Depends()]
