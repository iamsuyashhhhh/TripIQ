from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class DestinationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    country: str
    description: str
    category: str
    average_daily_cost: Decimal
    best_time_to_visit: str
    popularity_score: int
