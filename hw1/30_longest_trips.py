# /// script
# dependencies = ["sqlalchemy", "psycopg2-binary"]
# ///
import os

from sqlalchemy import create_engine, text

db_url = os.getenv('PSQL_DB_URL')
engine = create_engine(db_url)

query = """
SELECT 
   DATE(lpep_pickup_datetime) as pickup_date,
   lpep_pickup_datetime::TEXT || '->' || lpep_dropoff_datetime::TEXT as pikup_drop,
   total_amount,
   MAX(trip_distance) as max_distance
FROM taxi_trips
-- WHERE lpep_pickup_datetime >= '2019-10-01' 
-- AND lpep_pickup_datetime < '2019-11-01'
GROUP BY 1, 2, 3
ORDER BY max_distance DESC
LIMIT 5;
"""

with engine.connect() as conn:
    result = conn.execute(text(query)).fetchall()
    # the first result is suspiciously off
    for i, (ds, pikudrop, total, dist) in enumerate(result, start=1):
        print(
            f"{i}. Date: {ds}",
            f"Pickup/Drop: {pikudrop}",
            f"total_amount: {total}",
            f"Distance: {dist} miles",
            sep="\n  ",
        )
