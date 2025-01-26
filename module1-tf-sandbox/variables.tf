variable "gcp_project" {
  description = "GCP project id, like foo-bar-42069"
  type        = string
}

variable "gcp_region" {
  description = "GCP region, like us-central1"
  type        = string
  default     = "europe-north1"
}
