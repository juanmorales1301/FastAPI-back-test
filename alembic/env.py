from logging.config import fileConfig
import os
import sys
import importlib
from sqlalchemy import create_engine, pool
from alembic import context

# Añade el path de la aplicación al sistema para permitir el acceso a los módulos internos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.config.environments import settings  # Importa la configuración de la base de datos
from app.db.connect import Base  # Importa la Base de SQLAlchemy utilizada para los modelos

# Configura Alembic
config = context.config

# Configura el sistema de logging de Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Añade una función para importar dinámicamente todos los modelos desde la carpeta models
def import_all_models():
    # Busca la ruta de la carpeta models
    models_path = os.path.join(os.path.dirname(__file__), '..', 'app', 'models')
    
    # Itera sobre los archivos de la carpeta models y carga los modelos
    for filename in os.listdir(models_path):
        # Importa solo archivos .py y omite __init__.py
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f"app.models.{filename[:-3]}"  # Remueve la extensión .py para el nombre del módulo
            importlib.import_module(module_name)  # Importa el módulo dinámicamente

# Llama a la función para importar todos los modelos antes de establecer el target_metadata
import_all_models()

# Establece target_metadata con la metadata de la base de datos que utiliza SQLAlchemy
target_metadata = Base.metadata

# Define el proceso de migración en modo offline
def run_migrations_offline() -> None:
    """Ejecuta las migraciones en modo 'offline'.

    Configura el contexto de Alembic con una URL de conexión y no requiere un motor de base de datos.
    Las consultas SQL se emiten directamente a la salida del script en lugar de ejecutarse en una base de datos.
    """
    
    # Reemplaza 'asyncpg' con 'psycopg2' para usar el modo síncrono en las migraciones
    url = settings.DATABASE_URL.replace('asyncpg', 'psycopg2')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    # Ejecuta las migraciones dentro de una transacción
    with context.begin_transaction():
        context.run_migrations()

# Define el proceso de migración en modo online
def run_migrations_online() -> None:
    """Ejecuta las migraciones en modo 'online'.

    Configura Alembic para crear un motor de base de datos y conectar una sesión con el contexto de migración.
    """
    
    # Crea el motor de base de datos utilizando 'psycopg2' en lugar de 'asyncpg' para migraciones síncronas
    connectable = create_engine(
        settings.DATABASE_URL.replace('asyncpg', 'psycopg2'),
        poolclass=pool.NullPool
    )

    # Establece una conexión con el motor de base de datos
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        # Ejecuta las migraciones dentro de una transacción
        with context.begin_transaction():
            context.run_migrations()

# Determina si Alembic debe ejecutar las migraciones en modo online u offline
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
