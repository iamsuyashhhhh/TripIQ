from datetime import timedelta

from app.models import Itinerary, Trip


def build_itinerary(trip: Trip) -> dict:
    themes = ["Arrival and local highlights", "Culture, food, and neighborhoods", "Nature and signature experiences"]
    day_count = max((trip.end_date - trip.start_date).days + 1, 1)
    return {"days": [{"day": index + 1, "date": str(trip.start_date + timedelta(days=index)), "title": themes[index % len(themes)], "activities": [f"Explore {trip.destination.name}", "Local meal recommendation", "Flexible evening"]} for index in range(day_count)]}


def save_itinerary(trip: Trip, content: dict) -> None:
    if trip.itinerary:
        trip.itinerary.content = content
    else:
        trip.itinerary = Itinerary(trip_id=trip.id, content=content)
    trip.status = "planned"
