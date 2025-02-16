import rich
from q2_20_load_data import pipeline

if __name__ == '__main__':
    with pipeline.sql_client() as client:
        res = client.execute_sql(
            """
        SELECT
            avg(
                date_diff(
                    'minute',
                    trip_pickup_date_time,
                    trip_dropoff_date_time
                )
            ) 
        FROM rides;
            """
        )
    print(res)
