from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.core.user import User
from passlib.context import CryptContext

# Configuración de bcrypt para hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para obtener un usuario por nombre de usuario
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()

# Función para crear un nuevo usuario
async def create_user(db: AsyncSession, username: str, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    return user

# Función para verificar la contraseña
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Función para crear contraseña
def get_pass_hashed(password: str):
    return pwd_context.hash(password)