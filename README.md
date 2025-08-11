# Remote-vitals-streaming
Remote Patient Monitoring Pipeline!


remote-vitals-streaming/
├── .github/workflows/          # ← CREATE THESE
│   ├── terraform-plan.yml      # ← Runs on PRs
│   ├── terraform-apply.yml     # ← Runs on main branch
│   ├── terraform-validate.yml  # ← Validation & security
│   └── terraform-destroy.yml   # ← Manual cleanup
├── infra/                      # ← Your existing folder
│   ├── main.tf                 # ← Your existing file
│   ├── variables.tf            # ← Your existing file  
│   ├── versions.tf             # ← Update with backend config
│   ├── outputs.tf              # ← ADD THIS
│   └── rpm-dev.auto.tfvars     # ← Your existing file
└── docs/


Configure secrets in GitHub Settings > Secrets:

GCP_SA_KEY - Service account JSON
GCP_PROJECT_ID - Your project ID

 terraform state bucket: lucien-terraform-state-bucket