from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connect import get_db
from app.services.core.auth_service import create_access_token
from app.services.modules.user_services import create_user, get_user_by_username, verify_password, get_pass_hashed
from app.schemas.core.auth import UserCreate
from app.api.dependencies.auth_dependency import auth_required
from fastapi.security import OAuth2PasswordRequestForm
from app.services.core.response import new_response

auth_router = APIRouter()


# Ruta para registrar un nuevo usuario
@auth_router.post("/register", dependencies=[Depends(auth_required)])
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_user = await get_user_by_username(db, user.username)
        if db_user:
            return new_response({
                "mensaje": "El usuario ya está registrado.",
                "code": "IN0001",
                "status": 401
            })

        new_user = await create_user(db, user.username, user.email, user.password)
        return new_response({
            "mensaje": "Usuario registrado exitosamente.",
            "code": "IN0002"
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al registrar el usuario.")


# Ruta para login (autenticación)
@auth_router.post("/login")
async def login(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    try:
        db_user = await get_user_by_username(db, form_data.username)
        if not db_user or not verify_password(form_data.password, db_user.hashed_password):
            return new_response({
                "mensaje": "Usuario o contraseña incorrectos.",
                "code": "AU0001",
                "status": 401
            })
        # Generar token JWT
        access_token = create_access_token(data={"sub": db_user.username})
        return new_response({
            "mensaje": "Inicio de sesión exitoso.",
            "code": "AU0002",
            "data": {
                "user": db_user.username
            },
            "access_token": access_token,
            "token_type": "bearer"
        })
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error al iniciar sesión.")
