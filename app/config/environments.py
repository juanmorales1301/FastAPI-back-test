from pydantic_settings import BaseSettings

class Settings(BaseSettings):    
    TITLE: str = "API con FastAPI y JWT"
    DESCRIPTION: str = "Esta es una API utilizando FastAPI con autenticación JWT."
    VERSION: str = "1.0.0"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    TOKEN_URL: str = '/auth/login'

    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"
    SECRET_KEY: str
    DEBUG:  bool
    TIME_MIN_TOKEN: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = ""


settings = Settings()
