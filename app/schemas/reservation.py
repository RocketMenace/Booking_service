from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.table import Table


class ReservationBase(BaseModel):
    customer_name: str
    table_id: int
    duration_minutes: int
    reservation_time: datetime


class ReservationIn(ReservationBase):
    pass


class Reservation(ReservationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
