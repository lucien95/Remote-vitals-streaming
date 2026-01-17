# Remote state storage in GCS
# Uncomment after creating the bucket with: gsutil mb gs://kloudwithlucien-tfstate
terraform {
  backend "gcs" {
    bucket = "kloudwithlucien-tfstate"
    prefix = "remote-vitals-streaming"
  }
}
