import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config.settings import config
from app.main import app
from app.config.db import database

TEST_DATABASE_URL = f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_SERVER}:{config.POSTGRES_PORT}/test_booking_service"



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
        await conn.run_sync(config.Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(config.Base.metadata.drop_all)


@pytest.fixture
async def db_session(setup_db, async_engine):
    async with AsyncSession(
            async_engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
    ) as session:
        transaction = await session.begin()
        try:
            yield session
        finally:
            await transaction.rollback()
            await session.close()


@pytest.fixture
def override_get_db(db_session):
    async def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    return _override_get_db


@pytest.fixture
async def client(override_get_db):
    app.dependency_overrides[database.get_session] = override_get_db

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://127.0.0.1:8000/api",
            headers={"Content-Type": "application/json"}
    ) as client:
        yield client

    app.dependency_overrides.clear()
