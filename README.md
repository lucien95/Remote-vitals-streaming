# Remote Vitals Streaming

Real-time Remote Patient Monitoring (RPM) pipeline on Google Cloud Platform.

## Architecture

```
infra/              # Terraform infrastructure
.github/workflows/  # CI/CD pipelines
```

## Getting Started

### Prerequisites
- Google Cloud account with billing enabled
- Terraform >= 1.5.0
- `gcloud` CLI authenticated

### Deploy Infrastructure
```bash
cd infra
terraform init
terraform plan
terraform apply
```

## CI/CD

- **Pull requests** (from `feature/*` branches): Runs `terraform plan` and comments results
- **Push to main**: Applies infrastructure changes (requires environment approval)
