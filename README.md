## Proyecto FastAPI con Alembic y Virtualenv

Este proyecto es una API backend construida con **FastAPI**, **Uvicorn**, **Alembic** para la gestión de migraciones de base de datos y un entorno virtual gestionado con **virtualenv**.

### Contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución del proyecto](#ejecución-del-proyecto)
- [Comandos Alembic](#comandos-alembic)
- [Pruebas](#pruebas)
- [Documentación de la API](#documentación-de-la-api)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Comandos Uvicorn](#comandos-uvicorn)
- [Comandos adicionales](#comandos-adicionales)

---

### Requisitos

Antes de comenzar, asegúrate de tener instalados los siguientes requisitos en tu sistema:

- **Python 3.7+**
- **PostgreSQL** (u otra base de datos soportada)
- **virtualenv** (para la gestión del entorno virtual)
- **Git** (para el control de versiones)

---

### Instalación

1. **Clonar el repositorio:**

```bash
git clone https://github.com/usuario/proyecto-fastapi.git
cd proyecto-fastapi
```

2. **Crear un entorno virtual:**

```bash
python -m venv venv
```

3. **Activar el entorno virtual:**

- En **Windows**:
  ```bash
  venv\Scripts\activate
  ```

- En **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

4. **Instalar las dependencias:**

```bash
pip install -r requirements.txt
```

5. **Configurar el archivo `.env`:**

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@localhost:5432/NOMBRE_BD
SECRET_KEY=tu_clave_secreta
DEBUG=True
```

- Reemplaza `USER`, `PASSWORD` y `NOMBRE_BD` con los valores correspondientes a tu configuración de base de datos.

---

### Ejecución del proyecto

1. **Iniciar el servidor FastAPI:**

Para ejecutar la aplicación localmente, usa **Uvicorn**:

```bash
uvicorn app.main:app --reload
```

Esto iniciará el servidor en `http://127.0.0.1:8000`.

---

### Comandos Alembic

**Alembic** se usa para gestionar las migraciones de la base de datos. A continuación, se detallan algunos de los comandos más importantes:

1. **Inicializar Alembic**:

```bash
alembic init alembic
```

2. **Crear una nueva revisión de migración** (detecta cambios en los modelos y genera un script de migración):

```bash
alembic revision --autogenerate -m "Descripción de la migración"
```

3. **Aplicar las migraciones a la base de datos**:

```bash
alembic upgrade head
```

4. **Revertir la última migración**:

```bash
alembic downgrade -1
```

5. **Ver el historial de migraciones**:

```bash
alembic history
```

---

### Pruebas

Para ejecutar las pruebas del proyecto, utiliza **pytest**:

```bash
pytest
```

El reporte de pruebas se genera automáticamente.

---

### Documentación de la API

FastAPI genera automáticamente documentación interactiva para tu API.

1. **Documentación Swagger**:

Accede a la documentación interactiva de la API en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

2. **Documentación ReDoc**:

Accede a la documentación alternativa en formato ReDoc en [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

---

### Estructura del Proyecto (actualizada)

```bash
project-fastapi/
│
├── alembic/                      # Archivos de configuración de migraciones de Alembic
│   ├── versions/                 # Archivos de migración
│   └── env.py                    # Configuración de Alembic
│
├── app/
│   ├── api/                      # Rutas y middlewares
│   │   ├── dependencies/         # Dependencias para las rutas
│   │   ├── docs/                 # Documentación adicional
│   │   ├── errors/               # Gestión de errores centralizada
│   │   ├── middlewares/          # Middlewares personalizados
│   │   └── routes/               # Definición de rutas
│   │       └── router_api.py     # Centraliza todas las rutas
│   ├── config/                   # Configuraciones del proyecto
│   │   └── environments.py       # Variables de entorno y configuración del entorno
│   ├── db/                       # Conexión a la base de datos
│   │   ├── connect.py            # Conexión principal a la base de datos
│   │   └── init_db.py            # Inicialización de la base de datos
│   ├── models/                   # Definición de los modelos de la base de datos
│   │   ├── core/                 # Modelos principales
│   │   └── modules/              # Modelos relacionados a módulos específicos
│   ├── schemas/                  # Esquemas de Pydantic (validación de datos)
│   │   ├── core/                 # Esquemas principales
│   │   └── modules/              # Esquemas de módulos
│   ├── services/                 # Lógica de negocio
│   │   ├── core/                 # Servicios generales
│   │   └── modules/              # Servicios de módulos específicos
│   └── main.py                   # Punto de entrada de la aplicación FastAPI
│
├── tests/                        # Pruebas del proyecto
│
├── venv/                         # Entorno virtual (ignorado por Git)
│
├── .env                          # Variables de entorno (ignorado por Git)
├── .gitignore                    # Exclusiones para Git
├── alembic.ini                   # Archivo de configuración de Alembic
├── index.py                      # Archivo para ejecutar el proyecto
└── requirements.txt              # Dependencias del proyecto
```

---

### Comandos Uvicorn

**Uvicorn** es el servidor ASGI que se utiliza para ejecutar la aplicación FastAPI. Aquí están los comandos principales que puedes usar para ejecutar y configurar la aplicación:

1. **Ejecutar el servidor con recarga automática** (modo desarrollo):

```bash
uvicorn app.main:app --reload
```

Este comando iniciará el servidor FastAPI y habilitará la recarga automática cada vez que hagas cambios en el código.

2. **Especificar el host y el puerto**:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Esto ejecutará el servidor en `http://0.0.0.0:8000`, haciendo que esté disponible para otros dispositivos en la red.

3. **Ejecutar el servidor en modo producción**:

```bash
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
```

Este comando inicia el servidor con 4 trabajadores (para mejorar el rendimiento) y lo ejecuta en el host y puerto especificados.

4. **Ejecutar con configuración desde archivo `index.py`**:

Si tienes un archivo `index.py` en la raíz para iniciar el servidor, puedes usar:

```bash
python index.py
```

Este archivo debería contener la configuración de Uvicorn para ejecutar la aplicación, como:

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

---

### Comandos adicionales

1. **Instalar dependencias adicionales:**

Si necesitas instalar dependencias adicionales después de haber configurado el entorno:

```bash
pip install nombre_del_paquete
```

No olvides luego actualizar `requirements.txt`:

```bash
pip freeze > requirements.txt
```

2. **Desactivar el entorno virtual:**

Para desactivar el entorno virtual, usa el comando:

```bash
deactivate
```

---
