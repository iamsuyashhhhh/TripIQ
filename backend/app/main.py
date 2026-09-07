from datetime import date, timedelta
from decimal import Decimal

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models import Destination, Expense, Itinerary, Trip, User


app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://frontend:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "TripIQ API is running"}


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/v1/db-check")
def database_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "connected"}


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


def demo_user(db: Session) -> User:
    user = db.scalar(select(User).where(User.email == "demo@tripiq.app"))
    if not user:
        user = User(name="Demo Traveler", email="demo@tripiq.app", hashed_password="demo")
        db.add(user)
        db.flush()
    return user


def trip_payload(trip: Trip) -> dict:
    expenses = [
        {"id": expense.id, "category": expense.category, "description": expense.description,
         "estimated_amount": float(expense.estimated_amount), "currency": expense.currency}
        for expense in trip.expenses
    ]
    itinerary = trip.itinerary.content if trip.itinerary else None
    return {
        "id": trip.id, "title": trip.title, "destination": trip.destination.name,
        "country": trip.destination.country, "start_date": trip.start_date,
        "end_date": trip.end_date, "budget": float(trip.budget), "travelers": trip.travelers,
        "interests": trip.interests, "travel_style": trip.travel_style, "status": trip.status,
        "expenses": expenses, "itinerary": itinerary,
    }


@app.get("/api/v1/destinations", response_model=list[DestinationResponse])
def list_destinations(db: Session = Depends(get_db)):
    return db.scalars(select(Destination).order_by(Destination.popularity_score.desc())).all()


@app.get("/api/v1/destinations/search", response_model=list[DestinationResponse])
async def search_destinations(q: str, db: Session = Depends(get_db)):
    query = q.strip()
    if len(query) < 2:
        return []
    async with httpx.AsyncClient(timeout=8, headers={"User-Agent": "TripIQ/1.0 travel planner"}) as client:
        response = await client.get("https://geocoding-api.open-meteo.com/v1/search", params={"name": query, "count": 8, "language": "en", "format": "json"})
    response.raise_for_status()
    results = response.json().get("results", [])
    destinations = []
    seen = set()
    for result in results:
        name = result.get("name", query)
        country = result.get("country", "Unknown")
        key = (name, country)
        if key in seen:
            continue
        seen.add(key)
        destination = db.scalar(select(Destination).where(Destination.name == name, Destination.country == country))
        if not destination:
            destination = Destination(name=name, country=country, description=f"Plan a memorable trip to {name}.", category="city escape", average_daily_cost=150, best_time_to_visit="Anytime", popularity_score=70, latitude=result.get("latitude", 0), longitude=result.get("longitude", 0))
            db.add(destination)
            db.flush()
        destinations.append(destination)
    db.commit()
    return destinations


@app.get("/api/v1/trips")
def list_trips(db: Session = Depends(get_db)):
    user = demo_user(db)
    db.commit()
    trips = db.scalars(select(Trip).where(Trip.user_id == user.id).order_by(Trip.start_date)).all()
    return [trip_payload(trip) for trip in trips]


@app.post("/api/v1/trips")
def create_trip(payload: TripCreate, db: Session = Depends(get_db)):
    destination = db.get(Destination, payload.destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    if payload.end_date < payload.start_date:
        raise HTTPException(status_code=400, detail="End date must be after start date")
    user = demo_user(db)
    trip = Trip(user_id=user.id, **payload.model_dump())
    db.add(trip)
    db.flush()
    trip.itinerary = Itinerary(trip_id=trip.id, content={"days": []})
    db.commit()
    db.refresh(trip)
    return trip_payload(trip)


@app.post("/api/v1/trips/{trip_id}/generate")
def generate_itinerary(trip_id: int, db: Session = Depends(get_db)):
    trip = db.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    day_count = max((trip.end_date - trip.start_date).days + 1, 1)
    themes = ["Arrival and local highlights", "Culture, food, and neighborhoods", "Nature and signature experiences"]
    content = {"days": [{"day": index + 1, "date": str(trip.start_date + timedelta(days=index)),
                           "title": themes[index % len(themes)],
                           "activities": [f"Explore {trip.destination.name}", "Local meal recommendation", "Flexible evening"]}
                         for index in range(day_count)]}
    if trip.itinerary:
        trip.itinerary.content = content
    else:
        trip.itinerary = Itinerary(trip_id=trip.id, content=content)
    trip.status = "planned"
    db.commit()
    db.refresh(trip)
    return trip_payload(trip)


@app.post("/api/v1/trips/{trip_id}/expenses")
def add_expense(trip_id: int, payload: ExpenseCreate, db: Session = Depends(get_db)):
    trip = db.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    expense = Expense(trip_id=trip_id, **payload.model_dump())
    db.add(expense)
    db.commit()
    db.refresh(trip)
    return trip_payload(trip)
