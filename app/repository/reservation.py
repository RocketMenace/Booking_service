from typing import Annotated
from datetime import timedelta

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
                stmt = select(Reservation).where(
                    Reservation.reservation_time
                    < data["reservation_time"]
                    + timedelta(minutes=data["duration_minutes"]),
                    Reservation.end_time
                    > data["reservation_time"],
                    Reservation.table_id == data["table_id"],
                )
                res = await session.scalars(stmt)
                if res:
                    print("$$$$$$$$$$$$$$$$$$$$")
