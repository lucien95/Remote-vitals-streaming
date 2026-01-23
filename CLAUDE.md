# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Remote Patient Monitoring (RPM) streaming pipeline on Google Cloud Platform. A portfolio-ready cloud solution demonstrating healthcare data streaming architecture with production-grade security practices.

## Repository Structure

```
infra/                    # Terraform infrastructure
  ├── main.tf             # Core resources (Pub/Sub, Cloud Functions, FHIR)
  ├── workload-identity.tf # Keyless auth (Workload Identity Federation)
  ├── variables.tf        # Input variables
  └── backend.tf          # GCS remote state
app/
  ├── vitals-processor/   # Cloud Function (processes vitals → FHIR)
  └── simulator/          # Test tool (generates fake vitals)
.github/workflows/
  ├── terraform.yml       # Infra pipeline (with Checkov scanning)
  └── app-deploy.yml      # App pipeline
docs/images/              # Architecture diagrams
```

## Commands

### Terraform (run from `infra/` directory)
```bash
terraform init          # Initialize providers and backend
terraform fmt -check    # Check formatting
terraform validate      # Validate configuration
terraform plan          # Preview changes
terraform apply         # Apply changes
```

### Simulator (run from `app/simulator/` directory)
```bash
source venv/bin/activate
python vitals_simulator.py --count 10    # Send 10 vitals
python vitals_simulator.py --continuous  # Run continuously
```

### View Logs
```bash
gcloud functions logs read vitals-processor-dev --region=us-central1 --limit=20
```

## CI/CD Workflows

### Infrastructure Pipeline (`terraform.yml`)
- **Trigger:** Changes to `infra/`
- **Steps:** Checkov scan → Terraform fmt → init → validate → plan/apply
- **Auth:** Workload Identity Federation (keyless)

### App Pipeline (`app-deploy.yml`)
- **Trigger:** Changes to `app/vitals-processor/`
- **Steps:** Test → Deploy Cloud Function
- **Auth:** Workload Identity Federation (keyless)

## Authentication

This project uses **Workload Identity Federation** - no service account keys stored anywhere.

- Pool: `github-pool`
- Provider: `github-provider`
- Service Account: `terraform-ci@kloudwithlucien.iam.gserviceaccount.com`

## Key Architectural Decisions

1. **Pub/Sub for ingestion:** Decouples producers from consumers, provides durability
2. **Cloud Functions Gen2:** Serverless, auto-scales, pay-per-use
3. **FHIR R4:** Healthcare interoperability standard
4. **Workload Identity:** No stored credentials, short-lived tokens
5. **Checkov:** Security scanning before deployment

## Quality Checklist
- `terraform fmt` and `terraform validate` must pass
- Checkov scan must pass (or soft-fail acknowledged)
- Cloud Function logs show "Created Observation" on test
