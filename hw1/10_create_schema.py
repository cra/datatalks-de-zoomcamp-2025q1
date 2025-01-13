# /// script
# dependencies = [
#     "sqlalchemy",
#     "psycopg2-binary",
# ]
# ///
import os

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)

db_url = os.getenv('PSQL_DB_URL')
if not db_url:
    raise ValueError("PSQL_DB_URL environment variable is not set")

engine = create_engine(db_url)
metadata = MetaData()

taxi_zones = Table(
    'taxi_zones',
    metadata,
    Column('location_id', Integer, primary_key=True),
    Column('borough', String),
    Column('zone', String),
    Column('service_zone', String),
)

taxi_trips = Table(
    'taxi_trips',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('vendor_id', Integer),
    Column('lpep_pickup_datetime', DateTime),
    Column('lpep_dropoff_datetime', DateTime),
    Column('store_and_fwd_flag', String(1)),
    Column('ratecode_id', Integer),
    Column('pu_location_id', Integer, ForeignKey('taxi_zones.location_id')),
    Column('do_location_id', Integer, ForeignKey('taxi_zones.location_id')),
    Column('passenger_count', Integer),
    Column('trip_distance', Float),
    Column('fare_amount', Float),
    Column('extra', Float),
    Column('mta_tax', Float),
    Column('tip_amount', Float),
    Column('tolls_amount', Float),
    Column('ehail_fee', Float),
    Column('improvement_surcharge', Float),
    Column('total_amount', Float),
    Column('payment_type', Integer),
    Column('trip_type', Integer),
    Column('congestion_surcharge', Float),
)


def create_tables():
    metadata.create_all(engine)
    print("Tables created successfully!")


if __name__ == "__main__":
    create_tables()
