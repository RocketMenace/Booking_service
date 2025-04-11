from datetime import datetime

from sqlalchemy import DDL, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.db import database


class Reservation(database.Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    customer_name: Mapped[str] = mapped_column(String(length=50), nullable=False)
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"), nullable=False)
    table = relationship(
        "Table",
        back_populates="reservations",
        uselist=False,
    )
    reservation_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
