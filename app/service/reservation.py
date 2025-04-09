from typing import Annotated
from fastapi import Depends
from app.repository.reservation import ReservationRepository
from app.schemas.reservation import ReservationIn

class ReservationService:
    def __init__(self, repository: Annotated[ReservationRepository, Depends()]):
        self.repository = repository

    async def add_reservation(self, data: ReservationIn):
        data = data.model_dump()
        return await self.repository.add_one(data)

    async def get_reservations(self):
        return await self.repository.get_all()

    async def delete_reservation(self, reservation_id: int):
        return await self.repository.delete_one(reservation_id)