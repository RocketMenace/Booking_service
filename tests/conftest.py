import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.config.db import Database
from app.config.settings import config
from app.main import app
from app.models.table import Table

TEST_DATABASE_URL = f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_SERVER}:{config.POSTGRES_PORT}/test_booking_service"

database = Database(TEST_DATABASE_URL)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=True,
    )
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def setup_db(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.drop_all)


@pytest.fixture
async def db_session(setup_db, async_engine):
    async with AsyncSession(
        async_engine, expire_on_commit=False, autocommit=False, autoflush=False
    ) as session:
        transaction = await session.begin()
        try:
            yield session
        finally:
            await transaction.rollback()
            await session.close()


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://127.0.0.1:8000/api",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture
async def get_table_id(db_session):
    res = await db_session.execute(select(Table))
    table_id = res.scalars().first().id
    return table_id
