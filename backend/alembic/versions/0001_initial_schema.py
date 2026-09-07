"""Create TripIQ tables and seed destinations."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=20), server_default="USER", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )

    op.create_table(
        "destinations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("country", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("average_daily_cost", sa.Numeric(10, 2), nullable=False),
        sa.Column("best_time_to_visit", sa.String(length=120), nullable=False),
        sa.Column("popularity_score", sa.Integer(), nullable=False),
        sa.Column("latitude", sa.Numeric(9, 6), nullable=False),
        sa.Column("longitude", sa.Numeric(9, 6), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_destinations_country", "destinations", ["country"])
    op.create_index("ix_destinations_category", "destinations", ["category"])
    op.create_index("ix_destinations_popularity_score", "destinations", ["popularity_score"])

    op.create_table(
        "trips",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("destination_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("budget", sa.Numeric(10, 2), nullable=False),
        sa.Column("travelers", sa.Integer(), server_default="1", nullable=False),
        sa.Column("interests", sa.Text(), server_default="", nullable=False),
        sa.Column("travel_style", sa.String(length=80), server_default="balanced", nullable=False),
        sa.Column("status", sa.String(length=40), server_default="planning", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["destination_id"], ["destinations.id"], ondelete="RESTRICT"),
    )
    op.create_index("ix_trips_user_id", "trips", ["user_id"])
    op.create_index("ix_trips_destination_id", "trips", ["destination_id"])
    op.create_index("ix_trips_start_date", "trips", ["start_date"])

    op.create_table(
        "itineraries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("trip_id", sa.Integer(), nullable=False),
        sa.Column("content", postgresql.JSONB(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("trip_id", name="uq_itineraries_trip_id"),
    )

    op.create_table(
        "expenses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("trip_id", sa.Integer(), nullable=False),
        sa.Column("category", sa.String(length=40), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("estimated_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("currency", sa.String(length=3), server_default="USD", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_expenses_trip_id", "expenses", ["trip_id"])

    destinations = sa.table(
        "destinations",
        sa.column("name", sa.String),
        sa.column("country", sa.String),
        sa.column("description", sa.Text),
        sa.column("category", sa.String),
        sa.column("average_daily_cost", sa.Numeric),
        sa.column("best_time_to_visit", sa.String),
        sa.column("popularity_score", sa.Integer),
        sa.column("latitude", sa.Numeric),
        sa.column("longitude", sa.Numeric),
    )
    op.bulk_insert(destinations, [
        {"name": "Kyoto", "country": "Japan", "description": "Historic temples, quiet gardens, and traditional neighborhoods.", "category": "Culture", "average_daily_cost": 145, "best_time_to_visit": "March to May", "popularity_score": 95, "latitude": 35.0116, "longitude": 135.7681},
        {"name": "Lisbon", "country": "Portugal", "description": "Colorful streets, coastal viewpoints, and relaxed food culture.", "category": "City Break", "average_daily_cost": 110, "best_time_to_visit": "March to October", "popularity_score": 92, "latitude": 38.7223, "longitude": -9.1393},
        {"name": "Bali", "country": "Indonesia", "description": "Tropical beaches, rice terraces, temples, and wellness experiences.", "category": "Beach", "average_daily_cost": 80, "best_time_to_visit": "April to October", "popularity_score": 94, "latitude": -8.3405, "longitude": 115.0920},
        {"name": "Reykjavik", "country": "Iceland", "description": "A base for waterfalls, geothermal lagoons, and northern landscapes.", "category": "Adventure", "average_daily_cost": 210, "best_time_to_visit": "June to August", "popularity_score": 88, "latitude": 64.1466, "longitude": -21.9426},
        {"name": "Cape Town", "country": "South Africa", "description": "Mountain views, coastal drives, vineyards, and diverse neighborhoods.", "category": "Nature", "average_daily_cost": 95, "best_time_to_visit": "November to March", "popularity_score": 90, "latitude": -33.9249, "longitude": 18.4241},
    ])


def downgrade() -> None:
    op.drop_index("ix_expenses_trip_id", table_name="expenses")
    op.drop_table("expenses")
    op.drop_table("itineraries")
    op.drop_index("ix_trips_start_date", table_name="trips")
    op.drop_index("ix_trips_destination_id", table_name="trips")
    op.drop_index("ix_trips_user_id", table_name="trips")
    op.drop_table("trips")
    op.drop_index("ix_destinations_popularity_score", table_name="destinations")
    op.drop_index("ix_destinations_category", table_name="destinations")
    op.drop_index("ix_destinations_country", table_name="destinations")
    op.drop_table("destinations")
    op.drop_table("users")
