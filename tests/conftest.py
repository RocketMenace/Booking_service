import anyio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.config.settings import config
from app.main import app
from app.config.db import database

TEST_DATABASE_URL = f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_SERVER}:{config.POSTGRES_PORT}/test_booking_service"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
async def get_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000/api"
    ) as client:
        yield client


@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def create_db(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def db_session(create_db, async_engine):
    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        async with session.begin():
            yield session
            await session.rollback()
