from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
import uvicorn

from core import settings, close_connections
from api import main_router


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None, None]:
    # startup
    print("starting app...")
    yield
    # shoutdown
    print("closing app...")
    await close_connections()


app = FastAPI(lifespan=lifespan)
app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host=settings.uc.host, port=settings.uc.port, reload=settings.uc.reload)
