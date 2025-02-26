# /// script
# dependencies = ["google-cloud-storage", "rich"]
# ///

# src: https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/03-data-warehouse/load_yellow_taxi_data.py

import os
import pathlib
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import rich
from google.cloud import storage

# run with python upload_script $("terraform output -raw hw3-bucket-name")
BUCKET_NAME = sys.argv[1]
rich.print(BUCKET_NAME)

CREDENTIALS_FILE = os.getenv("TF_VAR_gcp_credentials_path")
client = storage.Client.from_service_account_json(CREDENTIALS_FILE)
bucket = client.bucket(BUCKET_NAME)

CHUNK_SIZE = 8 * 1024 * 1024


def verify_gcs_upload(blob_name):
    return storage.Blob(bucket=bucket, name=blob_name).exists(client)


def upload_to_gcs(file_path: pathlib.Path, max_retries=3):
    blob_name = file_path.name
    blob = bucket.blob(blob_name)
    blob.chunk_size = CHUNK_SIZE

    for attempt in range(max_retries):
        try:
            rich.print(f"Uploading {file_path} to {BUCKET_NAME} (Attempt {attempt + 1})...")
            blob.upload_from_filename(file_path)
            rich.print(f"Uploaded: gs://{BUCKET_NAME}/{blob_name}")

            if verify_gcs_upload(blob_name):
                rich.print(f"Verification successful for {blob_name}")
                return
            else:
                rich.print(f"Verification failed for {blob_name}, retrying...")
        except Exception as e:
            rich.print(f"Failed to upload {file_path} to GCS: {e}")

        time.sleep(5)

    rich.print(f"Giving up on {file_path} after {max_retries} attempts.")


if __name__ == "__main__":
    file_paths = [
        f"{dataset}_tripdata_{year}-{month:02d}.csv"
        for month in range(1, 13)
        for year in (2019, 2020)
        for dataset in ("fhv", "yellow", "green")
    ]
    rich.print(file_paths)

    with ThreadPoolExecutor(max_workers=6) as executor:
        executor.map(upload_to_gcs, map(pathlib.Path, file_paths))

    rich.print("All files processed and verified.")
