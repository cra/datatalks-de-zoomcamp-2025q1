# /// script
# dependencies = ["sqlalchemy", "psycopg2-binary"]
# ///
import os

from sqlalchemy import create_engine, text

db_url = os.getenv('PSQL_DB_URL')
engine = create_engine(db_url)

query = text(
    """
SELECT 
  COUNT(CASE WHEN trip_distance <= 1 AND trip_distance >= 0 THEN 1 END)
  as trips_under_1_mile,
  COUNT(CASE WHEN trip_distance > 1 AND trip_distance <= 3 THEN 1 END)
  as trips_from_1_to_3_mile,
  COUNT(CASE WHEN trip_distance > 3 AND trip_distance <= 7 THEN 1 END)
  as trips_from_3_to_7_mile,
  COUNT(CASE WHEN trip_distance > 7 AND trip_distance <= 10 THEN 1 END)
  as trips_from_7_to_10_mile,
  COUNT(CASE WHEN trip_distance > 10 THEN 1 END)
  as trips_over_10_miles,
  COUNT(*) as total_entries,
  COUNT(CASE WHEN trip_distance < 0 THEN 1 END)
  as negative_distances
FROM taxi_trips
--WHERE lpep_pickup_datetime >= '2019-10-01' 
--AND lpep_pickup_datetime < '2019-11-01'
"""
)

with engine.connect() as conn:
    result = conn.execute(query).fetchone()
    print("NB: THIS IS WITHOUT DATE FILTERING")
    print(f"Trips ≤ 1 mile: {result.trips_under_1_mile}")
    print(f"Trips (1; 3] mile: {result.trips_from_1_to_3_mile}")
    print(f"Trips (3; 7] mile: {result.trips_from_3_to_7_mile}")
    print(f"Trips (7; 10] mile: {result.trips_from_7_to_10_mile}")
    print(f"Trips > 10 miles: {result.trips_over_10_miles}")
    print(f"Negs: {result.negative_distances}")
    print(f"Total: {result.total_entries}")
