variable "gcp_project" {
  description = "GCP project id, like foo-bar-42069"
  type        = string
}

variable "gcp_credentials_path" {
  description = "GCP credentials like /path/to/file.json"
  type        = string
}

variable "gcp_region" {
  description = "GCP region, like us-central1"
  type        = string
  default     = "europe-north1"
}

variable "location" {
  description = "Project location"
  type        = string
  default     = "EU"
}
