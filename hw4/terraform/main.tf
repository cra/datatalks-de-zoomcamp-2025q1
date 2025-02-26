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

resource "google_storage_bucket" "hw4-bucket" {
  name          = "${var.gcp_project}-zoomcamp-hw4-bucket"
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

output "hw4-bucket-name" {
  value = google_storage_bucket.hw4-bucket.name
}

resource "google_bigquery_dataset" "hw4-gbq-dataset" {
  dataset_id = "hw4_taxi_trips"
  location   = var.location
}

##
# YELLOW
## 
resource "google_bigquery_table" "ext_yellow_tripdata" {
  dataset_id          = google_bigquery_dataset.hw4-gbq-dataset.dataset_id
  table_id            = "ext_yellow_tripdata"
  deletion_protection = false

  external_data_configuration {
    autodetect    = true
    source_format = "CSV"
    source_uris = [
      "gs://${google_storage_bucket.hw4-bucket.name}/yellow_tripdata_2019-*.csv",
      "gs://${google_storage_bucket.hw4-bucket.name}/yellow_tripdata_2020-*.csv"
    ]
  }
}

output "yellow_tripdata" {
  value = google_bigquery_table.ext_yellow_tripdata.table_id
}

##
# GREEN
## 
resource "google_bigquery_table" "ext_green_tripdata" {
  dataset_id          = google_bigquery_dataset.hw4-gbq-dataset.dataset_id
  table_id            = "ext_green_tripdata"
  deletion_protection = false

  external_data_configuration {
    autodetect    = true
    source_format = "CSV"
    source_uris = [
      "gs://${google_storage_bucket.hw4-bucket.name}/green_tripdata_2019-*.csv",
      "gs://${google_storage_bucket.hw4-bucket.name}/green_tripdata_2020-*.csv"
    ]
  }
}

output "green_tripdata" {
  value = google_bigquery_table.ext_green_tripdata.table_id
}


##
# FHV
## 
resource "google_bigquery_table" "ext_fhv_tripdata" {
  dataset_id          = google_bigquery_dataset.hw4-gbq-dataset.dataset_id
  table_id            = "ext_fhv_tripdata"
  deletion_protection = false

  external_data_configuration {
    autodetect    = true
    source_format = "CSV"
    source_uris = [
      "gs://${google_storage_bucket.hw4-bucket.name}/fhv_tripdata_2019-*.csv",
    ]
  }
}

output "fhv_tripdata" {
  value = google_bigquery_table.ext_fhv_tripdata.table_id
}
