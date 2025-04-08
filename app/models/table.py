from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.db import database
from app.models.reservation import Reservation


class Table(database.Base):
    __tablename__ = "tables"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=50), nullable=False)
    location: Mapped[str] = mapped_column(String(length=50), nullable=False)
    seats: Mapped[int] = mapped_column(Integer)
    reservations: Mapped[list["Reservation"]] = relationship(back_populates="table", cascade="all, delete-orphan")
