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
- 9 non-asset integration/unit tests pass.
- The local FastAPI service is running in development mode at
  `http://127.0.0.1:8000`.

## Cloud account checks

- AWS account `748998941962` is signed in. AWS Free Tier credit shows
  `US$100.00` issued, `US$0.00` used and `US$100.00` remaining, expiring
  `2027-08-27`.
- Alibaba Cloud is signed in as the primary account in `cn-hangzhou`.
- Alibaba Function Compute currently contains an existing unrelated
  `healthbridge-api` function. It must not be modified or deleted.
- No project resources have been created by this work yet.

## Current blockers

- The 30 supplied JPG fixtures are not present under
  `tests/fixtures/test_images/`.
- `models/mdv5a.pt` and `models/model.pt` are not present, so checksum tests
  and the real Worker smoke test cannot run.
- Terraform `1.13.2`, AWS CLI `1.46.0`, Alibaba Cloud CLI `3.4.11` and Docker
  Desktop are installed locally under `tools/` or the system application
  directory.
- WSL installation has been started with elevation, but Windows must be
  restarted before Docker Desktop can load the WSL 2 backend.
- Ubuntu is now installed and running under WSL 2. The Docker service is
  running, but Docker Desktop still reports that its backend cannot start.
- A full `terraform plan` is ready to run but is blocked until AWS and Alibaba
  CLI/provider credentials are configured locally; the signed-in browser
  session does not expose credentials to Terraform.
- The browser session is authenticated, but no AWS or Alibaba CLI credentials
  are configured locally. Do not create or commit access keys without an
  explicit credential-management decision.
- Cloud deployment inputs are still required: one AWS region, a globally
  unique Alibaba OSS bucket, a Cognito domain prefix, Function Compute
  endpoint and immutable image URIs.
- A private Git remote and teaching-team access must be configured by the
  team before submission.

## Next actions

1. Restore the supplied images and model weights, then rerun `pytest -q` and
   `scripts/preflight.ps1 -RunModelSmoke` after Worker dependencies are ready.
2. Install the deployment CLIs and Docker after confirming that software
   installation is allowed on this computer.
3. Review the Terraform plan and Function Compute configuration together,
   then apply cloud resources only after confirming billing consent.
4. Capture the live evidence listed in `PRE_SUBMISSION_CHECKLIST.md`.
