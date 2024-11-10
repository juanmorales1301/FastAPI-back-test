import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.exc import IntegrityError
from requests.exceptions import ConnectionError, Timeout
from fastapi.exceptions import RequestValidationError

logging.basicConfig(filename="error.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

def registrar_errores_handler(app: FastAPI):

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logging.error(f"HTTPException: {exc.status_code} - {exc.detail} - Path: {request.url.path}")
        return JSONResponse({"mensaje": exc.detail, "code": "AU0001", "correcto": False, "data": {}}, status_code=exc.status_code)

    @app.exception_handler(ExpiredSignatureError)
    async def token_expired_handler(request: Request, exc: ExpiredSignatureError):
        logging.error(f"Token expirado en la ruta: {request.url.path}")
        return JSONResponse({"mensaje": "El token ha expirado", "code": "AU0002", "correcto": False, "data": {}}, status_code=401)

    @app.exception_handler(InvalidTokenError)
    async def invalid_token_handler(request: Request, exc: InvalidTokenError):
        logging.error(f"Token inválido en la ruta: {request.url.path}")
        return JSONResponse({"mensaje": "Token inválido", "code": "AU0003", "correcto": False, "data": {}}, status_code=401)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logging.error(f"Error de validación: {exc.errors()} en la ruta: {request.url.path}")
        return JSONResponse({"mensaje": "Los datos enviados no son válidos", "code": "VA0001", "correcto": False, "data": {}}, status_code=422)

    @app.exception_handler(IntegrityError)
    async def db_integrity_error_handler(request: Request, exc: IntegrityError):
        logging.error(f"Error de integridad en la BD: {str(exc)} - Path: {request.url.path}")
        return JSONResponse({"mensaje": "Error en la base de datos", "code": "DB0001", "correcto": False, "data": {}}, status_code=400)

    @app.exception_handler(ConnectionError)
    async def connection_error_handler(request: Request, exc: ConnectionError):
        logging.error(f"Error de conexión: {str(exc)} - Path: {request.url.path}")
        return JSONResponse({"mensaje": "Error de conexión con servicio externo", "code": "TO0001", "correcto": False, "data": {}}, status_code=502)

    @app.exception_handler(Timeout)
    async def timeout_error_handler(request: Request, exc: Timeout):
        logging.error(f"Timeout: {str(exc)} - Path: {request.url.path}")
        return JSONResponse({"mensaje": "El servicio externo no respondió a tiempo", "code": "TO0002", "correcto": False, "data": {}}, status_code=504)

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logging.error(f"Error inesperado: {str(exc)} - Path: {request.url.path}")
        return JSONResponse({"mensaje": "Error interno, por favor intente nuevamente más tarde.", "code": "GE0001", "correcto": False, "data": {}}, status_code=500)
