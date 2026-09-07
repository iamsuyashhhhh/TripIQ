from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Index, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Destination(Base):
    __tablename__ = "destinations"
    __table_args__ = (
        Index("ix_destinations_country", "country"),
        Index("ix_destinations_category", "category"),
        Index("ix_destinations_popularity_score", "popularity_score"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    country: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(80))
    average_daily_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    best_time_to_visit: Mapped[str] = mapped_column(String(120))
    popularity_score: Mapped[int] = mapped_column(Integer)
    latitude: Mapped[Decimal] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Decimal] = mapped_column(Numeric(9, 6))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    trips: Mapped[list["Trip"]] = relationship(back_populates="destination")
