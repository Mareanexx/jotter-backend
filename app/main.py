from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api_v1 import api_router

app = FastAPI()

app.include_router(api_router)

app.mount("/uploads", StaticFiles(directory="media/uploads"), name="uploads")