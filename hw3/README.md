# Data Warehouse

eller, _BQ partitioning and clustering_

[homework itself](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/03-data-warehouse/homework.md)

**NB**, partitioned is a terrible word for my dislexia, so I tend to make it "partitoned" or "partoned". That was a source of a lot of issues

## sketchy walkthrough

A lot of tasks require you to use UI to look for some of the tips on some params, _but_

1. EXT table created using terraform, see [./main.tf](./terraform/main.tf)

2. Data uploaded using provided script, see [Makefile](./terraform/Makefile)

I was unable to figure out how to create the nonpartioned table in terraform though

3. then, open BQ studio and run some queries:

### queries to figure out the answers

DDL for nonpartioned table:
```sql
CREATE OR REPLACE TABLE `hw3_yellow_taxi.yellow_nonpartitioned`
SELECT * FROM `${var.gcp_project}.hw3_yellow_taxi.ext_yellow_tripdata`
```

queries themselves are straightforward, like:

```sql
SELECT count(DISTINCT PULocationID) FROM `hw3_yellow_taxi.ext_yellow_tripdata`
```

```sql
SELECT
  count(DISTINCT PULocationID),
  count(DISTINCT DOLocationID)
FROM `hw3_yellow_taxi.yellow_tripdata_nonpartitoned` 
```

```sql
SELECT
  count(*)
FROM `hw3_yellow_taxi.yellow_tripdata_nonpartitoned` 
WHERE fare_amount = 0
```

DDL for partitioned table:

```sql
CREATE OR REPLACE TABLE `hw3_yellow_taxi.yellow_partitioned`
  PARTITION BY DATE(tpep_dropoff_datetime)
  CLUSTER BY VendorID
  AS
SELECT * FROM `${var.gcp_project}.hw3_yellow_taxi.ext_yellow_tripdata`
```
