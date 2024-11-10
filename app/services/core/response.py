from pydantic import BaseModel
from fastapi import HTTPException
from typing import Optional, Dict


class response_model(BaseModel):
    status: Optional[int] = 200
    mensaje: str
    code: str
    correcto: Optional[bool] = True
    data: Optional[Dict] = {}
    access_token: Optional[str] = None
    token_type: Optional[str] = None


def new_response(retorno: response_model):
    # Convertir el diccionario a un objeto response_model para validar automáticamente
    try:
        retorno_valid = response_model(**retorno)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Si el status es >= 300, lanzar excepción HTTP
    if retorno_valid.status >= 300:
        raise HTTPException(
            status_code=retorno_valid.status, detail=retorno_valid.mensaje
        )

    # Devuelve la respuesta en formato de diccionario
    data_return = {
        "mensaje": retorno_valid.mensaje,
        "code": retorno_valid.code,
        "correcto": retorno_valid.correcto,
        "data": retorno_valid.data,
        "status_code": retorno_valid.status,
    }

    #Validaciones de retorno especiales
    if retorno_valid.access_token is not None:
        data_return["access_token"] = retorno_valid.access_token

    if retorno_valid.token_type is not None:
        data_return["token_type"] = retorno_valid.token_type

    return data_return
