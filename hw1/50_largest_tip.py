# /// script
# dependencies = ["sqlalchemy", "psycopg2-binary"]
# ///
import os

from sqlalchemy import create_engine, text

db_url = os.getenv('PSQL_DB_URL')
engine = create_engine(db_url)

query = """
SELECT 
    txt.lpep_pickup_datetime::TEXT || '->' || txt.lpep_dropoff_datetime::TEXT as pu_do,
   txt.tip_amount as tip,
   txt.total_amount as total,
   txz.zone as dropoff_zone
FROM taxi_trips txt
LEFT JOIN
  taxi_zones txz
  ON txt.do_location_id = txz.location_id
WHERE
    txt.pu_location_id = 74 -- East Harlem North
    AND DATE(txt.lpep_pickup_datetime) >= '2019-10-01' 
    AND DATE(txt.lpep_pickup_datetime) < '2019-11-01' 
ORDER BY tip DESC
LIMIT 5;
"""

with engine.connect() as conn:
    result = conn.execute(text(query)).fetchall()
    for i, (pu_do, tip, total, do_zone) in enumerate(result, start=1):
        print(
            f"{i}. Trip {pu_do}",
            f"East Harlem North -> {do_zone}",
            f"tip: {tip}. total: {total}.",
            sep="\n  ",
        )
