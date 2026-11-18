from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from api import main_router
from core import close_connections, settings
from fastapi import FastAPI


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

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.uc.host,
        port=settings.uc.port,
        reload=settings.uc.reload,
    )
