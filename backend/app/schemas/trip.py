from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class TripCreate(BaseModel):
    title: str
    destination_id: int
    start_date: date
    end_date: date
    budget: Decimal
    travelers: int = 1
    interests: str = ""
    travel_style: str = "balanced"


class ExpenseCreate(BaseModel):
    category: str
    description: str
    estimated_amount: Decimal
    currency: str = "USD"
