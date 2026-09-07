from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Trip(Base):
    __tablename__ = "trips"
    __table_args__ = (
        Index("ix_trips_user_id", "user_id"),
        Index("ix_trips_destination_id", "destination_id"),
        Index("ix_trips_start_date", "start_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    destination_id: Mapped[int] = mapped_column(ForeignKey("destinations.id", ondelete="RESTRICT"))
    title: Mapped[str] = mapped_column(String(160))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    budget: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    travelers: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    interests: Mapped[str] = mapped_column(Text, default="", server_default="")
    travel_style: Mapped[str] = mapped_column(String(80), default="balanced", server_default="balanced")
    status: Mapped[str] = mapped_column(String(40), default="planning", server_default="planning")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship(back_populates="trips")
    destination: Mapped["Destination"] = relationship(back_populates="trips")
    itinerary: Mapped["Itinerary | None"] = relationship(back_populates="trip", cascade="all, delete-orphan", uselist=False)
    expenses: Mapped[list["Expense"]] = relationship(back_populates="trip", cascade="all, delete-orphan")
