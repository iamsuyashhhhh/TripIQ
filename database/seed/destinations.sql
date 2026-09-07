-- The initial Alembic migration seeds these same destinations for a fresh database.
-- This standalone script is useful when refreshing only catalog data manually.
INSERT INTO destinations
    (name, country, description, category, average_daily_cost, best_time_to_visit, popularity_score, latitude, longitude)
VALUES
    ('Kyoto', 'Japan', 'Historic temples, quiet gardens, and traditional neighborhoods.', 'Culture', 145, 'March to May', 95, 35.0116, 135.7681),
    ('Lisbon', 'Portugal', 'Colorful streets, coastal viewpoints, and relaxed food culture.', 'City Break', 110, 'March to October', 92, 38.7223, -9.1393),
    ('Bali', 'Indonesia', 'Tropical beaches, rice terraces, temples, and wellness experiences.', 'Beach', 80, 'April to October', 94, -8.3405, 115.0920),
    ('Reykjavik', 'Iceland', 'A base for waterfalls, geothermal lagoons, and northern landscapes.', 'Adventure', 210, 'June to August', 88, 64.1466, -21.9426),
    ('Cape Town', 'South Africa', 'Mountain views, coastal drives, vineyards, and diverse neighborhoods.', 'Nature', 95, 'November to March', 90, -33.9249, 18.4241)
ON CONFLICT DO NOTHING;
