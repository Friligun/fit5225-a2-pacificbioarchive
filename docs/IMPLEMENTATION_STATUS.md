# Implementation Status

Updated 2026-08-28. This file records the current A2 readiness state without
credentials, tokens or other account secrets.

## Completed locally

- AWS + Alibaba Cloud architecture and deployment documentation are aligned.
- Terraform contains AWS resources plus the private Alibaba OSS model bucket.
- The Worker callback uses HMAC authentication and the Worker documentation
  describes Alibaba Function Compute.
- Local dependencies install cleanly (`pip check`).
- JavaScript and Python syntax checks pass.
- Terraform provider initialization and `terraform validate` pass without
  warnings.
- Full Python test suite passes: 16 tests.
- The local FastAPI service is running in development mode at
  `http://127.0.0.1:8000`.
- Python bytecode compilation for `app/`, `lambdas/` and `worker/` passes.
- The real local model smoke test passes on `Bos_taurus_1.JPG`, reporting model
  version `supplied-2026-08` and the tag `Bos_taurus: 6`.

## Cloud account checks

- AWS account `748998941962` is signed in. AWS Free Tier credit shows
  `US$100.00` issued, `US$0.00` used and `US$100.00` remaining, expiring
  `2027-08-27`.
- Alibaba Cloud provider credentials are configured for the Terraform plan in
  `cn-hangzhou`; no project resources have been created.
- Alibaba Function Compute currently contains an existing unrelated
  `healthbridge-api` function. It must not be modified or deleted.
- No project resources have been created by this work yet.

## Current blockers

- The supplied 30 JPG fixtures and both model files are restored locally and
  match the manifest SHA-256 checksums. The files remain ignored by Git.
- Terraform `1.13.2`, AWS CLI `1.46.0`, Alibaba Cloud CLI `3.4.11` and Docker
  Desktop are installed locally under `tools/` or the system application
  directory.
- Ubuntu is installed under WSL 2. Docker Desktop still cannot create its
  backend named pipe and logs `Access is denied`; restarting the Docker service
  requires administrator access.
- A read-only `terraform plan` succeeds with `26 to add, 0 to change, 0 to
  destroy`; it has not been applied.
- AWS identity checks succeed for account `748998941962`; Alibaba CLI account
  lookup needs a follow-up command, while the Terraform provider plan succeeds.
- Cloud deployment inputs are still required: one AWS region, a globally
  unique Alibaba OSS bucket, a Cognito domain prefix, Function Compute
  endpoint and immutable image URIs.
- The local repository is initialized on `main` and pushed to
  `https://github.com/Friligun/fit5225-a2-pacificbioarchive.git`; GitHub
  currently reports it as public, so an owner must change it to Private and
  invite the teaching team and all members.

## Next actions

1. Repair Docker Desktop's WSL 2 backend with administrator access, then build
   and scan the three images.
3. Fill the remaining Terraform inputs (immutable image URIs, private Worker
   endpoint and final HTTPS callback/logout URLs), configure encrypted remote
   state, and review the plan before any apply.
4. Change the GitHub repository to Private and invite the required accounts.
5. Capture the live evidence listed in `PRE_SUBMISSION_CHECKLIST.md`.
