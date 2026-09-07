# TripIQ

TripIQ is a ready-to-run travel planning MVP. It lets you search real destinations, create trips, generate day-by-day plans, and track expenses:

- React + Vite + Tailwind frontend
- FastAPI backend
- PostgreSQL database
- Docker Compose wiring
- SQLAlchemy models and relationships
- Alembic migration for the complete initial schema
- Seed destinations for local development
- Live destination search through geocoding
- Trip planning with budget, dates, travelers, interests, and travel style
- Itinerary generation and expense tracking

## Start

```bash
docker compose up --build
```

The backend container runs `alembic upgrade head` before starting FastAPI.

## Verify

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Health check: http://localhost:8000/api/v1/health
- Database check: http://localhost:8000/api/v1/db-check

## Phase 2 database commands

Run migrations locally from `backend/` when working outside Docker:

```bash
alembic upgrade head
alembic current
```

The initial migration creates `users`, `destinations`, `trips`, `itineraries`, and `expenses`, then seeds five destinations. The standalone SQL seed is in `database/seed/destinations.sql`. Search results are stored as destinations when selected.

## GitHub upload

This repository intentionally excludes dependencies, secrets, Python caches, build output, and local Docker data. Copy `backend/.env.example` and `frontend/.env.example` only when local environment configuration is needed.
