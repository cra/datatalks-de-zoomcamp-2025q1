# Analytics engineering

[homework itself](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/04-analytics-engineering/homework.md)

learning dbt and some modeling

## Taxi data

Start by creating downloading all assets and gunzipping:

```bash
cd terraform
make dl-assets
make -j6 gunzip_all
```

total zipped: 2.4G, total unzipped: 13G

## Setup

Check [envrc_template](./terraform/envrc_template) to make sure you have proper env vars set up. Create GCS bucket:

```bash
terraform init
terraform apply # fail on bq step
```

The second command fails because it tries to create tables as well, but there's no data. Let's fix that:

```bash
make upload
```

Uploading files takes some time (30 mins or so).
Eventually, run terraform to create the external tables once all the files are in the bucket:

```bash
terraform apply
```

### Data check

Run some basic counts to check that we have correct number of rows, something like:

```sql
SELECT 'yellow' as tag, count(*) as _has, '109,047,158' as _want FROM `hw4_taxi_trips.ext_yellow_tripdata` 
UNION ALL
SELECT 'green' as tag, count(*) as _has, '7,778,101' as _want FROM `hw4_taxi_trips.ext_green_tripdata` 
UNION ALL
SELECT 'fhv' as tag, count(*) as _has, '43,244,696' as _want FROM `hw4_taxi_trips.ext_fhv_tripdata`
```

## Init dbt

I'm using dbt core (locally) with bigquery (in da cloud). So it's inbetween alternatives, _nice_.

```bash
uv init
uv add dbt-core dbt-bigquery
uv run dbt init
```

Answering some questions will make sure you end up with a profile saved in `~/.dbt/profiles.yml`

The resulting project is in the same folder as this readme file. To test connection:

```bash
dbt debug
```

## Modeling

Staging model copied from [the setup](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/5ad8dbb1e0425d14fce5e42270124d76d736d6f4/04-analytics-engineering/taxi_rides_ny/models/staging) and dim/facts were added, as instructed in the hw

To build dev views/tables:

```bash
uv run dbt build
```

To build prod views/tables:
```bash
uv run dbt build --vars '{'is_test_run': 'false'}'
```

