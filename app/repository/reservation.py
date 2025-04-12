from typing import Annotated
from datetime import timedelta, datetime

from fastapi import Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import database
from app.models.reservation import Reservation
from app.repository.base import BaseRepository


class ReservationRepository(BaseRepository):
    def __init__(self, session: Annotated[AsyncSession, Depends(database.get_session)]):
        self.session = session
        super().__init__(session, Reservation)

    async def add_one(self, data):
        async with self.session as session:
            async with session.begin():
                stmt = select(Reservation).where(Reservation.table_id == data.get("table_id"))
                res = await session.execute(stmt)

