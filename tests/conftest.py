from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import core.db.transactional as transactional
from app.models import Base
from core.config import config
from core.db import get_session
from core.server import app

engine = create_async_engine(config.POSTGRES_TEST_URL.unicode_string(), pool_pre_ping=True)

async_session_local = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def override_get_session() -> AsyncGenerator:
    async with async_session_local() as session:
        yield session
        await session.commit()


app.dependency_overrides[get_session] = override_get_session


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncSession:
    async_engine = engine
    async_session = async_session_local

    async with async_session() as session:
        async with async_engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        transactional.session = session
        yield session

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        pass

    await async_engine.dispose()


@pytest_asyncio.fixture(scope="module")
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
