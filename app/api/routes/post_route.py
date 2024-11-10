from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connect import get_db
from app.services.modules.post_services import create_post, get_posts
from app.schemas.modules.posts import PostCreate
from app.api.dependencies.auth_dependency import auth_required

post_router = APIRouter()

@post_router.post("/posts", dependencies=[Depends(auth_required)])
async def create_new_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_post = await create_post(db, post.title, post.content, post.author_id)
        return {
            "mensaje": "Post creado exitosamente.",
            "code": "IN0001",  # Código para insertar
            "correcto": True,
            "data": new_post
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear el post.")

@post_router.get("/posts", dependencies=[Depends(auth_required)])
async def read_posts(db: AsyncSession = Depends(get_db)):
    try:
        posts = await get_posts(db)
        return {
            "mensaje": "Consulta exitosa.",
            "code": "CO0001",  # Código para consulta
            "correcto": True,
            "data": posts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al consultar los posts.")
