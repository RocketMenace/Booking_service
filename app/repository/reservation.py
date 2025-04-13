from typing import Annotated
from datetime import timedelta

from fastapi import Depends
from sqlalchemy import select, insert, text, exists
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import database
from app.core.exceptions import ReservationExistsError
from app.models.reservation import Reservation
from app.repository.base import BaseRepository


class ReservationRepository(BaseRepository):
    def __init__(self, session: Annotated[AsyncSession, Depends(database.get_session)]):
        self.session = session
        super().__init__(session, Reservation)

    async def add_one(self, data):
        async with self.session as session:
            async with session.begin():
                new_reservation_ending = data.get("reservation_time") + timedelta(
                    minutes=data.get("duration_minutes")
                )
                stmt = select(exists().where(
                    Reservation.table_id == data.get("table_id"),
                    Reservation.reservation_time <= new_reservation_ending,
                    Reservation.reservation_time
                    + (Reservation.duration_minutes * text("interval '1 minute'"))
                    >= data["reservation_time"],
                ))
                if await session.scalar(stmt):
                    raise ReservationExistsError(
                        detail=f"Table with id: {data.get('table_id')} already reserved."
                    )
                ins_stmt = insert(Reservation).values(data).returning(Reservation)
                result = await session.execute(ins_stmt)
                return result.scalar().__dict__
