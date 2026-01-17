# -----------------------------------------------------------------------------
# Cloud Healthcare API - FHIR Store for patient vitals
# -----------------------------------------------------------------------------

resource "google_healthcare_dataset" "vitals" {
  name     = "vitals-${var.environment}"
  location = var.region
}

resource "google_healthcare_fhir_store" "observations" {
  name    = "observations"
  dataset = google_healthcare_dataset.vitals.id
  version = "R4"

  enable_update_create          = true
  disable_referential_integrity = false

  notification_configs {
    pubsub_topic = google_pubsub_topic.fhir_notifications.id
  }
}

# -----------------------------------------------------------------------------
# Pub/Sub - Message ingestion and FHIR notifications
# -----------------------------------------------------------------------------

resource "google_pubsub_topic" "vitals_ingest" {
  name = "vitals-ingest-${var.environment}"
}

resource "google_pubsub_topic" "fhir_notifications" {
  name = "fhir-notifications-${var.environment}"
}

resource "google_pubsub_subscription" "vitals_processor" {
  name  = "vitals-processor-${var.environment}"
  topic = google_pubsub_topic.vitals_ingest.id

  ack_deadline_seconds = 60

  push_config {
    push_endpoint = google_cloudfunctions2_function.vitals_processor.url
    oidc_token {
      service_account_email = google_service_account.function_invoker.email
    }
  }
}

# -----------------------------------------------------------------------------
# Service Accounts
# -----------------------------------------------------------------------------

resource "google_service_account" "vitals_processor" {
  account_id   = "vitals-processor-${var.environment}"
  display_name = "Vitals Processor Cloud Function"
}

resource "google_service_account" "function_invoker" {
  account_id   = "function-invoker-${var.environment}"
  display_name = "Pub/Sub Function Invoker"
}

# Grant FHIR editor to the processor
resource "google_healthcare_fhir_store_iam_member" "processor_fhir" {
  fhir_store_id = google_healthcare_fhir_store.observations.id
  role          = "roles/healthcare.fhirResourceEditor"
  member        = "serviceAccount:${google_service_account.vitals_processor.email}"
}

# Grant invoker permission
resource "google_cloudfunctions2_function_iam_member" "invoker" {
  project        = var.project_id
  location       = var.region
  cloud_function = google_cloudfunctions2_function.vitals_processor.name
  role           = "roles/cloudfunctions.invoker"
  member         = "serviceAccount:${google_service_account.function_invoker.email}"
}

# Grant run invoker for Gen2 functions
resource "google_cloud_run_service_iam_member" "invoker" {
  project  = var.project_id
  location = var.region
  service  = google_cloudfunctions2_function.vitals_processor.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.function_invoker.email}"
}

# -----------------------------------------------------------------------------
# Cloud Storage - Function source code
# -----------------------------------------------------------------------------

resource "google_storage_bucket" "function_source" {
  name     = "${var.project_id}-functions-${var.environment}"
  location = var.region

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}

resource "google_storage_bucket_object" "function_source" {
  name   = "vitals-processor-${data.archive_file.function_source.output_md5}.zip"
  bucket = google_storage_bucket.function_source.name
  source = data.archive_file.function_source.output_path
}

data "archive_file" "function_source" {
  type        = "zip"
  source_dir  = "${path.module}/../app/vitals-processor"
  output_path = "${path.module}/.tmp/vitals-processor.zip"
}

# -----------------------------------------------------------------------------
# Cloud Function - Vitals Processor
# -----------------------------------------------------------------------------

resource "google_cloudfunctions2_function" "vitals_processor" {
  name     = "vitals-processor-${var.environment}"
  location = var.region

  build_config {
    runtime     = "python311"
    entry_point = "process_vitals"

    source {
      storage_source {
        bucket = google_storage_bucket.function_source.name
        object = google_storage_bucket_object.function_source.name
      }
    }
  }

  service_config {
    max_instance_count = 10
    min_instance_count = 0
    available_memory   = "256M"
    timeout_seconds    = 60

    service_account_email = google_service_account.vitals_processor.email

    environment_variables = {
      FHIR_STORE_PATH = google_healthcare_fhir_store.observations.id
      PROJECT_ID      = var.project_id
    }
  }
}
