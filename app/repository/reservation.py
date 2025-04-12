from typing import Annotated
from datetime import timedelta, datetime

from fastapi import Depends
from sqlalchemy import select, insert
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
                stmt = select(Reservation).where(
                    Reservation.table_id == data.get("table_id")
                )
                res = await session.execute(stmt)
                for record in res.scalars().all():
                    if record.reservation_time <= data.get(
                        "reservation_time"
                    ) + timedelta(
                        minutes=data.get("duration_minutes")
                    ) and record.reservation_time + timedelta(
                        minutes=record.duration_minutes
                    ) >= data.get("reservation_time"):
                        raise ReservationExistsError(
                            detail=f"Table with {data.get('table_id')} already reserved."
                        )
                ins = insert(Reservation).values(data).returning(Reservation)
                r = await session.execute(ins)
