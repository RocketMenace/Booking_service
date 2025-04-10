from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.schemas.reservation import Reservation, ReservationIn
from app.service.reservation import ReservationService

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post(path="", status_code=status.HTTP_201_CREATED, response_model=Reservation)
async def create_reservation(
    data: ReservationIn, service: Annotated[ReservationService, Depends()]
):
    return await service.add_reservation(data)


@router.get(path="", status_code=status.HTTP_200_OK, response_model=list[Reservation])
async def get_reservations(service: Annotated[ReservationService, Depends()]):
    return await service.get_reservations()


@router.delete(path="/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(
    reservation_id: int, service: Annotated[ReservationService, Depends()]
):
    return await service.delete_reservation(reservation_id)
