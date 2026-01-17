output "fhir_store_id" {
  description = "Full path to FHIR store"
  value       = google_healthcare_fhir_store.observations.id
}

output "pubsub_topic" {
  description = "Pub/Sub topic for vitals ingestion"
  value       = google_pubsub_topic.vitals_ingest.id
}

output "function_url" {
  description = "Cloud Function URL"
  value       = google_cloudfunctions2_function.vitals_processor.url
}

output "function_service_account" {
  description = "Service account used by the Cloud Function"
  value       = google_service_account.vitals_processor.email
}
