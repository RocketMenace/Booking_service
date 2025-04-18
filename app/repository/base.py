from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import TypeVar

from app.config.db import database
from app.core.exceptions import NotFoundError

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
                stmt = insert(self.model).values(data).returning(self.model)
                res = await session.execute(stmt)
                return res.scalar().__dict__

    async def get_all(self):
        async with self.session as session:
            result = await session.execute(select(self.model))
            return result.scalars().all()

    async def delete_one(self, obj_id: int):
        async with self.session as session:
            async with session.begin():
                obj = await session.get(self.model, obj_id)
                if not obj:
                    raise NotFoundError(detail=f"Object with id: {obj_id} not found")
                return await session.delete(obj)
