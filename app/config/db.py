from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base

from app.config.settings import config

DATABASE_URL = f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_SERVER}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"


class Database:
    def __init__(self):
        self.engine = create_async_engine(DATABASE_URL, echo=True, future=True)
        self.Base = declarative_base()

    async def create_db(self, db_name: str):
        try:
            async with self.engine.connect() as conn:
                result = await conn.execute(
                    text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
                )
                db_exists = result.scalar()
                if not db_exists:
                    await conn.execute(text(f'CREATE DATABASE "{db_name}"'))
                    print(f"Database '{db_name}' created successfully")
                else:
                    print(f"Database '{db_name}' already exists")
        except ProgrammingError as e:
            print(f"Error creating database: {e}")
        finally:
            await self.engine.dispose()

    async def ping_db(self):
        try:
            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            print("Successfully connected to the Database")
        except Exception as e:
            print(f"Error connecting to the Database: {e}")

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)
        print("Database tables created successfully")

    async def clear_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.drop_all)
        print("Database CLEARED!!!!")

    @asynccontextmanager
    async def get_session(self):
        async_session = async_sessionmaker(self.engine, class_=AsyncSession)
        session = None
        try:
            session = async_session()
            async with session:
                yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

    async def close_db(self):
        await self.engine.dispose()
        print("Database connection closed")


database = Database()


async def setup_db():
    await database.create_db("booking_service")
    await database.ping_db()
    await database.create_tables()
