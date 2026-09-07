from datetime import date

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Destination, Expense, Itinerary, Trip, User
from app.schemas.destination import DestinationResponse
from app.schemas.trip import ExpenseCreate, TripCreate
from app.services.trip_service import build_itinerary, save_itinerary

router = APIRouter()


@router.get("/")
def root():
    return {"message": "TripIQ API is running"}


@router.get("/api/v1/health")
def health_check():
    return {"status": "ok"}


@router.get("/api/v1/db-check")
def database_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "connected"}


def demo_user(db: Session) -> User:
    user = db.scalar(select(User).where(User.email == "demo@tripiq.app"))
    if not user:
        user = User(name="Demo Traveler", email="demo@tripiq.app", hashed_password="demo")
        db.add(user)
        db.flush()
    return user


def trip_payload(trip: Trip) -> dict:
    return {"id": trip.id, "title": trip.title, "destination": trip.destination.name, "country": trip.destination.country, "start_date": trip.start_date, "end_date": trip.end_date, "budget": float(trip.budget), "travelers": trip.travelers, "interests": trip.interests, "travel_style": trip.travel_style, "status": trip.status, "expenses": [{"id": item.id, "category": item.category, "description": item.description, "estimated_amount": float(item.estimated_amount), "currency": item.currency} for item in trip.expenses], "itinerary": trip.itinerary.content if trip.itinerary else None}


@router.get("/api/v1/destinations", response_model=list[DestinationResponse])
def list_destinations(db: Session = Depends(get_db)):
    return db.scalars(select(Destination).order_by(Destination.popularity_score.desc())).all()


@router.get("/api/v1/destinations/search", response_model=list[DestinationResponse])
async def search_destinations(q: str, db: Session = Depends(get_db)):
    query = q.strip()
    if len(query) < 2:
        return []
    async with httpx.AsyncClient(timeout=8, headers={"User-Agent": "TripIQ/1.0 travel planner"}) as client:
        response = await client.get("https://geocoding-api.open-meteo.com/v1/search", params={"name": query, "count": 8, "language": "en", "format": "json"})
    response.raise_for_status()
    destinations = []
    seen = set()
    for result in response.json().get("results", []):
        name, country = result.get("name", query), result.get("country", "Unknown")
        if (name, country) in seen:
            continue
        seen.add((name, country))
        destination = db.scalar(select(Destination).where(Destination.name == name, Destination.country == country))
        if not destination:
            destination = Destination(name=name, country=country, description=f"Plan a memorable trip to {name}.", category="city escape", average_daily_cost=150, best_time_to_visit="Anytime", popularity_score=70, latitude=result.get("latitude", 0), longitude=result.get("longitude", 0))
            db.add(destination)
            db.flush()
        destinations.append(destination)
    db.commit()
    return destinations


@router.get("/api/v1/trips")
def list_trips(db: Session = Depends(get_db)):
    user = demo_user(db)
    db.commit()
    return [trip_payload(trip) for trip in db.scalars(select(Trip).where(Trip.user_id == user.id).order_by(Trip.start_date)).all()]


@router.post("/api/v1/trips")
def create_trip(payload: TripCreate, db: Session = Depends(get_db)):
    if payload.end_date < payload.start_date:
        raise HTTPException(status_code=400, detail="End date must be after start date")
    destination = db.get(Destination, payload.destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    trip = Trip(user_id=demo_user(db).id, **payload.model_dump())
    db.add(trip)
    db.flush()
    trip.itinerary = Itinerary(trip_id=trip.id, content={"days": []})
    db.commit()
    db.refresh(trip)
    return trip_payload(trip)


@router.post("/api/v1/trips/{trip_id}/generate")
def generate_itinerary(trip_id: int, db: Session = Depends(get_db)):
    trip = db.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    save_itinerary(trip, build_itinerary(trip))
    db.commit()
    db.refresh(trip)
    return trip_payload(trip)


@router.post("/api/v1/trips/{trip_id}/expenses")
def add_expense(trip_id: int, payload: ExpenseCreate, db: Session = Depends(get_db)):
    trip = db.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    db.add(Expense(trip_id=trip_id, **payload.model_dump()))
    db.commit()
    db.refresh(trip)
    return trip_payload(trip)
