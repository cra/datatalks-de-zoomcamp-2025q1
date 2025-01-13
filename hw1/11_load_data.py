# /// script
# dependencies = [
#     "sqlalchemy",
#     "pandas",
#     "psycopg2-binary",
# ]
# ///

import gzip
import os
from urllib.parse import urlparse

import psycopg2


def main():
    # Parse DB URL
    db_url = os.getenv('PSQL_DB_URL')
    parsed = urlparse(db_url)
    db_params = {
        'dbname': parsed.path[1:],
        'user': parsed.username,
        'password': parsed.password,
        'host': parsed.hostname,
        'port': parsed.port,
    }

    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Load zones
    with open(os.getenv('TAXI_ZONES'), 'r') as f:
        cur.copy_expert(
            """
COPY taxi_zones(location_id, borough, zone, service_zone) 
FROM STDIN WITH (FORMAT CSV, HEADER true)
            """,
            f,
        )

    with gzip.open(os.getenv('TAXI_TRIPS'), 'rt') as f:
        cur.copy_expert(
            """
COPY taxi_trips(
    vendor_id, lpep_pickup_datetime, lpep_dropoff_datetime,
    store_and_fwd_flag, ratecode_id, pu_location_id, do_location_id,
    passenger_count, trip_distance, fare_amount, extra, mta_tax,
    tip_amount, tolls_amount, ehail_fee, improvement_surcharge,
    total_amount, payment_type, trip_type, congestion_surcharge
) FROM STDIN WITH (FORMAT CSV, HEADER true)
        """,
            f,
        )

    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
