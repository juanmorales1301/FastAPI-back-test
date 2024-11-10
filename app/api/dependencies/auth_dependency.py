from fastapi import Depends, HTTPException
from app.services.core.auth_service import get_current_user

# Dependencia que protege una ruta con autenticación
async def auth_required(current_user: str = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Autentificación requerida")
    return current_user
