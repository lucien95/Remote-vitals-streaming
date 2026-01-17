#!/usr/bin/env python3
"""
Vitals Simulator - Generates fake patient vital signs and publishes to Pub/Sub.

Usage:
    python vitals_simulator.py                    # Send 10 readings
    python vitals_simulator.py --count 50         # Send 50 readings
    python vitals_simulator.py --continuous       # Run continuously (Ctrl+C to stop)
"""

import argparse
import json
import random
import time
from datetime import datetime, timezone

from google.cloud import pubsub_v1

# Configuration
PROJECT_ID = "kloudwithlucien"
TOPIC_ID = "vitals-ingest-dev"

# Simulated patients
PATIENTS = ["patient-001", "patient-002", "patient-003", "patient-004", "patient-005"]


def generate_vital(patient_id: str, vital_type: str) -> dict:
    """Generate a single vital sign reading."""

    vital_ranges = {
        "heart_rate": {"min": 60, "max": 100, "unit": "bpm"},
        "spo2": {"min": 94, "max": 100, "unit": "%"},
        "blood_pressure_systolic": {"min": 100, "max": 140, "unit": "mmHg"},
        "blood_pressure_diastolic": {"min": 60, "max": 90, "unit": "mmHg"},
        "temperature": {"min": 36.1, "max": 37.5, "unit": "Cel"},
        "respiratory_rate": {"min": 12, "max": 20, "unit": "/min"},
    }

    config = vital_ranges[vital_type]

    # Add some randomness - occasionally generate abnormal values
    if random.random() < 0.1:  # 10% chance of abnormal
        if vital_type == "heart_rate":
            value = random.choice([random.randint(40, 59), random.randint(101, 120)])
        elif vital_type == "spo2":
            value = random.randint(88, 93)
        elif vital_type == "temperature":
            value = round(random.uniform(37.6, 39.0), 1)
        else:
            value = random.uniform(config["min"], config["max"])
    else:
        if vital_type == "temperature":
            value = round(random.uniform(config["min"], config["max"]), 1)
        elif vital_type in ["heart_rate", "spo2", "respiratory_rate"]:
            value = random.randint(int(config["min"]), int(config["max"]))
        else:
            value = random.randint(int(config["min"]), int(config["max"]))

    return {
        "patient_id": patient_id,
        "type": vital_type,
        "value": value,
        "unit": config["unit"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def generate_patient_vitals(patient_id: str) -> list:
    """Generate a complete set of vitals for a patient."""

    vital_types = [
        "heart_rate",
        "spo2",
        "blood_pressure_systolic",
        "blood_pressure_diastolic",
        "temperature",
        "respiratory_rate",
    ]

    return [generate_vital(patient_id, vt) for vt in vital_types]


def publish_vital(publisher, topic_path: str, vital: dict) -> None:
    """Publish a vital reading to Pub/Sub."""

    data = json.dumps(vital).encode("utf-8")
    future = publisher.publish(topic_path, data)
    message_id = future.result()

    print(f"  [{vital['patient_id']}] {vital['type']}: {vital['value']} {vital['unit']} (msg: {message_id})")


def run_simulator(count: int = 10, continuous: bool = False, interval: float = 2.0):
    """Run the vitals simulator."""

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

    print(f"Publishing to: {topic_path}")
    print("-" * 50)

    readings_sent = 0

    try:
        while continuous or readings_sent < count:
            patient = random.choice(PATIENTS)
            vitals = generate_patient_vitals(patient)

            print(f"\nSending vitals for {patient}:")
            for vital in vitals:
                publish_vital(publisher, topic_path, vital)
                readings_sent += 1

                if not continuous and readings_sent >= count:
                    break

            if continuous or readings_sent < count:
                time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\nSimulator stopped.")

    print(f"\nTotal readings sent: {readings_sent}")


def main():
    parser = argparse.ArgumentParser(description="Simulate patient vital signs")
    parser.add_argument("--count", type=int, default=10, help="Number of readings to send")
    parser.add_argument("--continuous", action="store_true", help="Run continuously")
    parser.add_argument("--interval", type=float, default=2.0, help="Seconds between batches")

    args = parser.parse_args()
    run_simulator(count=args.count, continuous=args.continuous, interval=args.interval)


if __name__ == "__main__":
    main()
