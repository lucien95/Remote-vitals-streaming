## Goal
Build a portfolio-ready SME cloud solution. Priorities:
1) Working deployment
2) Security + cost awareness
3) Excellent docs
4) Publish-ready content pack

## Repo structure
- infra/ (Terraform)
- app/ (service code)
- docs/ (architecture + runbook)
- content/ (drafts for LinkedIn/Medium/Substack)
- .github/workflows/ (CI)

## Quality bar before "done"
- terraform fmt/validate passes
- app tests pass
- README has: problem, architecture, quickstart, cost notes, security notes
- docs/runbook.md exists
- content pack generated

## Commands to use
- make test
- make lint
- make terraform-validate
- make dev

## Content tone
Professional, direct, human. No hype. Clear steps. Include "who this helps" + "how to run".