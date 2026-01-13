# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Remote Patient Monitoring (RPM) streaming pipeline on Google Cloud Platform. A portfolio-ready SME cloud solution demonstrating healthcare data streaming architecture.

## Repository Structure

```
infra/           # Terraform infrastructure (GCP resources)
.github/workflows/  # CI/CD (Terraform plan on PR, apply on main)
app/             # Service code (planned)
docs/            # Architecture documentation (planned)
content/         # Content drafts for publishing (planned)
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

### CI/CD Workflow
- PRs from `feature/*` branches to `main` trigger: fmt check, validate, plan (commented on PR)
- Pushes to `main` trigger: terraform apply (requires `production` environment approval)
- Only runs when files in `infra/` change

## Required Secrets (GitHub Actions)
- `GCP_SA_KEY`: Service account JSON credentials
- `GCP_PROJECT_ID`: Target GCP project ID

## Quality Checklist
- `terraform fmt` and `terraform validate` must pass
- README includes: problem statement, architecture, quickstart, cost notes, security notes
- `docs/runbook.md` exists before considering "done"
