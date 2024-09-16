import asyncio

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import core.db.transactional as transactional
from app.models import Base
from core.config import config

engine = create_async_engine(config.POSTGRES_TEST_URL.unicode_string(), pool_pre_ping=True)

async_session_local = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """
    Create an event loop for the entire test session.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncSession:
    """
    Creates a new database session and initializes the database schema for each test module.
    """
    async with async_session_local() as session:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        transactional.session = session
        yield session

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
    await engine.dispose()
