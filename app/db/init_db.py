import os
import importlib
from sqlalchemy.ext.asyncio import AsyncEngine
from app.db.connect import Base

# Función para cargar dinámicamente todos los modelos desde la carpeta models
def import_all_models():
    models_path = os.path.join(os.path.dirname(__file__), '..', 'models')
    
    # Itera sobre todos los archivos .py en la carpeta models
    for filename in os.listdir(models_path):
        if filename.endswith('.py') and filename != '__init__.py':
            # Construye el nombre del módulo dinámicamente
            module_name = f"app.models.{filename[:-3]}"
            importlib.import_module(module_name)

# Función para crear todas las tablas en la base de datos de manera dinámica
async def create_tables(engine: AsyncEngine):
    # Importa todos los modelos antes de crear las tablas
    import_all_models()
    
    async with engine.begin() as conn:        
        await conn.run_sync(Base.metadata.create_all) # Ejecuta la creación de las tablas
