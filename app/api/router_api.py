from fastapi import APIRouter
from app.api.routes.auth_route import auth_router
from app.api.routes.post_route import post_router

api_router = APIRouter()


api_router.include_router(auth_router, prefix="/auth", tags=["auth"]) # Modulo de autentificación
api_router.include_router(post_router, prefix="/posts", tags=["posts"]) # Modulo de Posts
