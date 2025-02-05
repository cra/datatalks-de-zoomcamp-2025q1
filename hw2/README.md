# Orchestration

[homework itself](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/02-workflow-orchestration/homework.md)


## Walkthrough

I'm on linux, so I had to change the postgresql address to point to `postgres_zoomcamp` in connection, and update `docker-compose.yml` accordingly.

I imported workflows using curl and then updated them in the UI. The `02_postgres_taxi.yaml` needed to be updated to have options for other years.

I used `02_postgres_taxi_scheduled.yaml` with backfill range of 2021-jan-01 till 2021-dec-31 for both yellow and green taxi. I was dropping green/yellow tables using pgadmin between answering row count questions to make sure I only get relevant data.

The row count is simply done with a pg query similar to this one:

```sql
SELECT COUNT(*), 'staging' FROM public.green_tripdata_staging
UNION ALL
SELECT COUNT(*), 'datamart' FROM public.green_tripdata
```

For the timezone question, just check the docs
