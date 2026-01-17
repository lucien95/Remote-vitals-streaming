import base64
import json
import os
import functions_framework
import google.auth
import google.auth.transport.requests
import requests as http_requests


FHIR_STORE_PATH = os.environ.get("FHIR_STORE_PATH")
PROJECT_ID = os.environ.get("PROJECT_ID")
HEALTHCARE_API_URL = "https://healthcare.googleapis.com/v1"


def get_access_token():
    """Get access token for Healthcare API."""
    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-healthcare"]
    )
    credentials.refresh(google.auth.transport.requests.Request())
    return credentials.token


@functions_framework.http
def process_vitals(request):
    """Process incoming vitals from Pub/Sub and store in FHIR."""

    envelope = request.get_json()
    if not envelope:
        return ("Bad Request: no Pub/Sub message received", 400)

    if not isinstance(envelope, dict) or "message" not in envelope:
        return ("Bad Request: invalid Pub/Sub message format", 400)

    pubsub_message = envelope["message"]

    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        data = base64.b64decode(pubsub_message["data"]).decode("utf-8")
        vitals = json.loads(data)
    else:
        return ("Bad Request: no data in Pub/Sub message", 400)

    try:
        observation = create_fhir_observation(vitals)
        result = store_observation(observation)
        print(f"Created Observation: {result.get('id')}")
        return ("OK", 200)
    except Exception as e:
        print(f"Error processing vitals: {e}")
        return (f"Error: {e}", 500)


def create_fhir_observation(vitals: dict) -> dict:
    """Convert vitals data to FHIR Observation resource."""

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
            "coding": [get_vital_code(vitals.get("type", "unknown"))],
            "text": vitals.get("type", "Unknown Vital")
        },
        "subject": {
            "reference": f"Patient/{vitals.get('patient_id', 'unknown')}"
        },
        "effectiveDateTime": vitals.get("timestamp"),
        "valueQuantity": {
            "value": vitals.get("value"),
            "unit": vitals.get("unit", ""),
            "system": "http://unitsofmeasure.org"
        }
    }

    return observation


def get_vital_code(vital_type: str) -> dict:
    """Get LOINC code for vital type."""

    codes = {
        "heart_rate": {
            "system": "http://loinc.org",
            "code": "8867-4",
            "display": "Heart rate"
        },
        "spo2": {
            "system": "http://loinc.org",
            "code": "2708-6",
            "display": "Oxygen saturation"
        },
        "blood_pressure_systolic": {
            "system": "http://loinc.org",
            "code": "8480-6",
            "display": "Systolic blood pressure"
        },
        "blood_pressure_diastolic": {
            "system": "http://loinc.org",
            "code": "8462-4",
            "display": "Diastolic blood pressure"
        },
        "temperature": {
            "system": "http://loinc.org",
            "code": "8310-5",
            "display": "Body temperature"
        },
        "respiratory_rate": {
            "system": "http://loinc.org",
            "code": "9279-1",
            "display": "Respiratory rate"
        }
    }

    return codes.get(vital_type, {
        "system": "http://loinc.org",
        "code": "unknown",
        "display": "Unknown"
    })


def store_observation(observation: dict) -> dict:
    """Store FHIR Observation in Healthcare API using REST."""

    access_token = get_access_token()

    url = f"{HEALTHCARE_API_URL}/{FHIR_STORE_PATH}/fhir/Observation"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/fhir+json"
    }

    response = http_requests.post(url, headers=headers, json=observation)
    response.raise_for_status()

    return response.json()
