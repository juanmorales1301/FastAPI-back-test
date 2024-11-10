from fastapi import FastAPI
from app.api.router_api import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.config.environments import settings
from app.db.connect import engine
from app.db.init_db import create_tables

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

from app.api.errors.handlers import registrar_errores_handler
registrar_errores_handler(app)


@app.on_event("startup")
async def on_startup():
    await create_tables(engine) # Llama a la función que crea las tablas de manera dinámica
