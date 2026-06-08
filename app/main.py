from fastapi import FastAPI
from core import settings
import uvicorn


app = FastAPI()

if __name__ == '__main__':
    uvicorn.run("main:app", host=settings.uc.host, port=settings.uc.port, reload=settings.uc.reload)
