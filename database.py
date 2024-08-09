from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from models import Base

DATABASE_URL = "sqlite+aiosqlite:///./shop.db"

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with async_session() as session:
        yield session


async def delete_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
