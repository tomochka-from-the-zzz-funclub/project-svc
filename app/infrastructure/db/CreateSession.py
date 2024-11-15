from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.infrastructure.db.Settings import get_db_url

DATABASE_URL = get_db_url()

# Создаем асинхронный движок
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем фабрику сессий для асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)