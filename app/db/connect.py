from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config.environments import settings

Base = declarative_base() # Define la base para los modelos


engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True) # Crea el motor asíncrono

async_session = sessionmaker( # Permite sesiones asincronas
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():# Provee sesiones asíncronas
    async with async_session() as session:
        yield session
