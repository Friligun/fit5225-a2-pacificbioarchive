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
- 8 non-asset integration/unit tests pass when run directly; the full suite
  currently reports 9 passed and 7 failures caused by missing supplied assets.
- The local FastAPI service is running in development mode at
  `http://127.0.0.1:8000`.
- Python bytecode compilation for `app/`, `lambdas/` and `worker/` passes.

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

1. Restore the supplied images, model weights and a short demonstration video;
   then rerun `pytest -q` and `scripts/preflight.ps1 -RunModelSmoke`.
2. Repair Docker Desktop's WSL 2 backend, then build and scan the three images.
3. Fill the remaining Terraform inputs (immutable image URIs, private Worker
   endpoint and final HTTPS callback/logout URLs), configure encrypted remote
   state, and review the plan before any apply.
4. Change the GitHub repository to Private and invite the required accounts.
5. Capture the live evidence listed in `PRE_SUBMISSION_CHECKLIST.md`.
