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

resource "google_storage_bucket" "demo-bucket" {
  name          = "${var.gcp_project}-terra-bucket"
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

resource "google_bigquery_dataset" "demo-dataset" {
  dataset_id = "demo_dataset"
  location   = var.location
}
