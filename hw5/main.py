import datetime
import os

import pyspark  # noqa
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def test_setup(spark, csv_fname):
    df = spark.read.option("header", "true").csv(csv_fname)

    df.show()
    print("Hello from local-spark!")

    print("writing data to parquet, see './zones'")
    df.write.parquet("zones", mode="overwrite")


def q2(spark, fname):
    df = spark.read.parquet(fname).repartition(4)
    df.write.parquet("q2", mode="overwrite")
    print("to answer Q2, see du -hs ./q2/part*")


def q3(spark, fname, day):
    df = spark.read.parquet(fname).repartition(4)
    # use df.columns to check column name
    # use df.head() to check date
    left = F.column("tpep_pickup_datetime") >= day
    right = F.column("tpep_pickup_datetime") < day + datetime.timedelta(days=1)
    total_trips = df.filter(left & right).count()
    print("Q3:", total_trips)


def q4(spark, fname):
    df = spark.read.parquet(fname).repartition(4)
    df = df.withColumn("t0", F.unix_timestamp("tpep_pickup_datetime"))
    df = df.withColumn("t1", F.unix_timestamp("tpep_dropoff_datetime"))
    df = df.withColumn("tdiff_h", ((F.col("t1") - F.col("t0")) / 3600).cast("bigint"))
    longest_trip = df.agg({"tdiff_h": "max"}).collect()[0][0]
    print("Q4:", longest_trip)


def q6(spark, trips_fname, zones_fname):
    trips = spark.read.parquet(trips_fname).repartition(4)
    pu_counts = trips.groupBy("PULocationID").count()
    zones = spark.read.option("header", "true").csv(zones_fname)
    query = (
        pu_counts.join(zones, zones["LocationID"] == pu_counts["PULocationID"])
        .select("Zone", "count")
        .sort("count", ascending=True)
    )
    print("Q6:")
    query.show(5, truncate=False)


if __name__ == "__main__":
    spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()
    zones_fname = os.getenv("ZONES_LOOKUP_CSV_FILENAME")
    trips_fname = os.getenv("YELLOW_2024OCTOBER_TRIPS_PARQUET_FILENAME")

    test_setup(spark, zones_fname)

    print("Q1:", spark.version)
    q2(spark, trips_fname)
    q3(spark, trips_fname, datetime.datetime(2024, 10, 15))
    q4(spark, trips_fname)
    print("Q5:", spark.sparkContext.uiWebUrl)
    q6(spark, trips_fname, zones_fname)
