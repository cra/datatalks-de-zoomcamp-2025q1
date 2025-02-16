terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.17.0"
    }
  }
}

provider "google" {
  credentials = file(var.gcp_credentials_path)
  project     = var.gcp_project
  region      = var.gcp_region
}

resource "google_storage_bucket" "hw3-bucket" {
  name          = "${var.gcp_project}-zoomcamp-hw3-bucket"
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

output "hw3-bucket-name" {
  value = google_storage_bucket.hw3-bucket.name
}

resource "google_bigquery_dataset" "hw3-bq-dataset" {
  dataset_id = "hw3_yellow_taxi"
  location   = var.location
}

resource "google_bigquery_table" "ext_yellow_tripdata" {
  dataset_id          = google_bigquery_dataset.hw3-bq-dataset.dataset_id
  table_id            = "ext_yellow_tripdata"
  deletion_protection = false

  external_data_configuration {
    autodetect    = true
    source_format = "PARQUET"
    source_uris = [
      "gs://${google_storage_bucket.hw3-bucket.name}/yellow_tripdata_2024-0*.parquet"
    ]
  }
}

# THIS DIDN'T WORK 🤷🏻
# resource "google_bigquery_table" "yellow_tripdata_non_partitioned" {
#   dataset_id = google_bigquery_dataset.hw3-bq-dataset.dataset_id
#   table_id   = "yellow_tripdata_nonpartioned"

#   deletion_protection = false
# }

# resource "google_bigquery_job" "query_job" {
#   job_id = "job_query_${google_bigquery_table.yellow_tripdata_non_partitioned.table_id}"

#   query {
#     query          = <<-EOF
#     CREATE OR REPLACE TABLE
#     `${google_bigquery_dataset.hw3-bq-dataset.dataset_id}.${google_bigquery_table.yellow_tripdata_non_partitioned.table_id}`
#     AS SELECT
#       *
#     FROM `${google_bigquery_dataset.hw3-bq-dataset.dataset_id}.${google_bigquery_table.ext_yellow_tripdata.table_id}`
#     EOF
#     use_legacy_sql = false
#   }

#   depends_on = [
#     google_bigquery_table.ext_yellow_tripdata,
#     google_bigquery_table.yellow_tripdata_non_partitioned
#   ]
# }


# output "non_partitioned_table_name" {
#   value = google_bigquery_table.yellow_tripdata_non_partitioned.table_id
# }

