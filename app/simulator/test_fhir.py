#!/usr/bin/env python3
"""Test FHIR API directly to see error details."""

import json
from datetime import datetime, timezone
import google.auth
import google.auth.transport.requests
import requests

FHIR_STORE_PATH = "projects/kloudwithlucien/locations/us-central1/datasets/vitals-dev/fhirStores/observations"
HEALTHCARE_API_URL = "https://healthcare.googleapis.com/v1"


def get_access_token():
    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-healthcare"]
    )
    credentials.refresh(google.auth.transport.requests.Request())
    return credentials.token


def test_create_observation():
    observation = {
        "resourceType": "Observation",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "vital-signs",
                        "display": "Vital Signs"
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "8867-4",
                    "display": "Heart rate"
                }
            ],
            "text": "heart_rate"
        },
        "subject": {
            "reference": "Patient/test-patient-001"
        },
        "effectiveDateTime": datetime.now(timezone.utc).isoformat(),
        "valueQuantity": {
            "value": 72,
            "unit": "bpm",
            "system": "http://unitsofmeasure.org"
        }
    }

    print("Observation to create:")
    print(json.dumps(observation, indent=2))
    print("\n" + "=" * 50 + "\n")

    access_token = get_access_token()
    url = f"{HEALTHCARE_API_URL}/{FHIR_STORE_PATH}/fhir/Observation"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/fhir+json"
    }

    print(f"POST {url}")
    response = requests.post(url, headers=headers, json=observation)

    print(f"\nStatus: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")


if __name__ == "__main__":
    test_create_observation()
