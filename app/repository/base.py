from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import TypeVar

from app.config.db import database

DBModel = TypeVar("DBModel", bound=database.Base)


class BaseRepository:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(database.get_session)],
        model: DBModel,
    ):
        self.session = session
        self.model = model

    async def add_one(self, data: dict[str, Any]):
        async with self.session as session:
            async with session.begin():
                session.add(self.model(**data))
