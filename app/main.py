from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api_v1 import api_router

app = FastAPI()

app.include_router(api_router)

app.mount("/uploads", StaticFiles(directory="media/uploads"), name="uploads")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True, limit_max_requests=5 * 1024 * 1024)
