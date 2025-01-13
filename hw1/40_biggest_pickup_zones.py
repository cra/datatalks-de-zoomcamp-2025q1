# /// script
# dependencies = ["sqlalchemy", "psycopg2-binary"]
# ///
import os

from sqlalchemy import create_engine, text

db_url = os.getenv('PSQL_DB_URL')
engine = create_engine(db_url)

query = """
SELECT 
   sum(total_amount) as total_amount,
   txz.zone
FROM taxi_trips txt
LEFT JOIN
  taxi_zones txz
  ON txt.pu_location_id = txz.location_id
WHERE DATE(txt.lpep_pickup_datetime) = '2019-10-18' 
GROUP BY 2
HAVING sum(total_amount) > 13000
ORDER BY total_amount DESC
LIMIT 5;
"""

with engine.connect() as conn:
    result = conn.execute(text(query)).fetchall()
    # the first result is suspiciously off
    for i, (total, zone) in enumerate(result, start=1):
        print(f"{i}. Zone: {zone}, total: {total}.")
