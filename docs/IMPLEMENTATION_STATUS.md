# Implementation Status

Updated 2026-08-28. This file records the current A2 readiness state without
credentials, tokens or other account secrets.

## Completed locally

- AWS + Alibaba Cloud architecture and deployment documentation are aligned.
- Terraform contains AWS resources plus the private Alibaba OSS model bucket.
- The Worker callback uses HMAC authentication and the Worker documentation
  describes Alibaba Function Compute.
- Worker dependencies are installed and the real model smoke test passes. The
  local environment reports a third-party protobuf constraint warning because
  MegaDetector pins `protobuf<=3.20.1` while ONNX 1.22 requests a newer range.
- JavaScript and Python syntax checks pass.
- Terraform provider initialization and `terraform validate` pass without
  warnings.
- Full Python test suite passes: 16 tests.
- The local FastAPI service is running in development mode at
  `http://127.0.0.1:8000`.
- Python bytecode compilation for `app/`, `lambdas/` and `worker/` passes.
- The real local model smoke test passes on `Bos_taurus_1.JPG`, reporting model
  version `supplied-2026-08` and the tag `Bos_taurus: 6`.
- All three local container images build successfully. The API reports HTTP 200
  in production mode, the Dispatcher handles an empty SQS event, and the Worker
  `/healthz` endpoint reports HTTP 200 on CPU.

## Cloud account checks

- AWS account `748998941962` is signed in. AWS Free Tier credit shows
  `US$100.00` issued, `US$0.00` used and `US$100.00` remaining, expiring
  `2027-08-27`.
- AWS core resources are deployed in `ap-southeast-2`; the API Gateway
  `$default` stage is auto-deployed and `/api/health` returns HTTP 200.
- The Cognito client callback and logout URLs use the deployed API HTTPS origin.
- Alibaba OSS model bucket and Function Compute Worker are deployed in
  `cn-hangzhou`; the Worker uses a scoped OSS-read execution role.
- Alibaba Function Compute also contains an existing unrelated `healthbridge-api`
  function; it was not modified.

## Current blockers

- The supplied 30 JPG fixtures and both model files are restored locally and
  match the manifest SHA-256 checksums. The files remain ignored by Git.
- Terraform `1.13.2`, AWS CLI `1.46.0`, Alibaba Cloud CLI `3.4.11` and Docker
  Desktop are installed locally under `tools/` or the system application
  directory.
- Ubuntu is installed under WSL 2 and Docker daemon is running after an
  administrator restart. Docker Hub base images are reachable; the AWS Lambda
  public ECR base image remains unreachable through the current network, so the
  API and Dispatcher use the AWS Lambda Runtime Interface Client on the tested
  Python base image instead.
- The encrypted remote Terraform backend is configured, but the local Terraform
  client currently times out when listing the S3 state bucket. The live API
  Gateway stage therefore still needs to be imported into state.
- AWS and Alibaba identity checks succeed, and API, Dispatcher and Worker image
  URIs are digest-pinned in the untracked deployment variables.
- The local repository is initialized on `main` and pushed to
  `https://github.com/Friligun/fit5225-a2-pacificbioarchive.git`; GitHub
  currently reports it as public, so an owner must change it to Private and
  invite the teaching team and all members.

## Next actions

1. Capture the live Cognito, upload, processing, search, bulk-edit, deletion and
   SNS evidence listed in `PRE_SUBMISSION_CHECKLIST.md`.
2. Run the supplied 30-image model evaluation and retain the accuracy table.
3. Scan the published images and import the API Gateway stage into Terraform
   state when the S3 backend endpoint is reachable.
4. Complete the architecture/demo video and team/individual reports.
