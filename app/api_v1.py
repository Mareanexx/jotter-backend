from fastapi import APIRouter
from app.routers import user, profile, article, like, follows, comment, report, auth, collection

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user.router)
api_router.include_router(profile.router)
api_router.include_router(article.router)
api_router.include_router(collection.router)
api_router.include_router(like.router)
api_router.include_router(follows.router)
api_router.include_router(comment.router)
api_router.include_router(report.router)
api_router.include_router(auth.router)
