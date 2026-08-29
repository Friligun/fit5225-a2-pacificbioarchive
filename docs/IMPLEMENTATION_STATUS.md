# Implementation Status

Updated 2026-08-29. This file records the current A2 readiness state without
credentials, tokens or other account secrets.

## Completed locally

- AWS + Alibaba Cloud architecture and deployment documentation are aligned.
- Terraform contains AWS resources plus the private Alibaba OSS model bucket.
- The Worker callback uses HMAC authentication and the Worker documentation
  describes Alibaba Function Compute.
- Worker dependencies are installed and the real model smoke test passes.
- The real supplied-model evaluation over all 30 labelled fixtures reports
  27/30 correct (90%); the three false predictions are recorded in
  `tmp/model-evaluation-summary.json` for transparent reporting.
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

## Current cloud verification

- The published Worker image is digest-pinned in Alibaba Function Compute with
  8192 MB memory, 4 vCPU and a 900-second timeout.
- A requeued production image completed successfully: DynamoDB reached `READY`,
  the compressed thumbnail was written, and the model tag was persisted.
- Direct online `/query` verification returned HTTP 200 with model version
  `supplied-2026-08` and tag `alectura_lathami`.
- SNS email subscription for `felis_catus` was confirmed successfully; AWS
  reports one confirmed subscription and no pending confirmations.
- Final `scripts/preflight.ps1` passed with 16 Python tests and Terraform
  validation. Unauthenticated `GET /api/media` returned HTTP `401`.
- A 2026-08-29 recheck confirmed public `/api/health` HTTP 200 and production
  Cognito session state, but the authenticated media-list request still
  returned HTTP 401; no destructive or mutating action was attempted.
- Following re-authentication, the UI loaded media records, accepted a
  temporary `felis_catus` tag, and returned only the target record for the
  combined `felis_catus:1, bos_taurus:1` search.
- `Felis_catus_3.JPG` reached `READY` with the model tag `felis_catus x 1`.
  The QQ mailbox received the live SNS message `Pacific BioArchive:
  felis_catus detected` with event `tag-added`. The temporary tag on
  `Bos_taurus_1.JPG` remains in place until explicitly requested otherwise.
- After re-authentication, a duplicate upload of `Bos_taurus_1.JPG` returned
  `Ready: Bos_taurus_1.JPG`; the archive remained at three records and retained
  the original media ID `ce5ae836-19fa-48e5-850b-490833b74f29`. This confirms
  checksum-based duplicate handling without a second media record.
- The supplied `video.mp4` uploaded successfully as media ID
  `66d273fd-edba-4628-a9a1-78882d943191`, but remained
  `video | processing | not classified` after approximately four minutes.
  Thumbnail generation, one-frame-per-second evidence and aggregate tags
  initially appeared blocked by the deployed processing path.
- On 2026-08-29 the Alibaba Function Compute `/healthz` check was adjusted to
  allow the large worker image up to 180 seconds to start (10-second probe,
  six failures tolerated). The existing video then completed without a second
  upload: DynamoDB reports `READY`, thumbnail path present, model version
  `supplied-2026-08`, and aggregate tags for eight species.
- The API Lambda timeout was increased from 30 to 300 seconds because
  query-by-file invokes the remote model synchronously and can include a cold
  start. Terraform now records the same 300-second timeout.
- A second Cognito user (`ypei0023@student.monash.edu`) is now confirmed and
  signed in. Its archive is empty and the original user's media remain
  isolated; the ownership resolver explicitly returned `Thumbnail URL is not
  owned by this user`.
- ECR scans for the API and Dispatcher `security-20260829-v2` image digests
  completed successfully. The scan status is `COMPLETE`; AWS reports 4
  critical, 8 high, 5 medium and 1 low finding for each image. These findings
  are inherited from the Python/Debian base layer (including OpenSSL, glibc,
  Perl and SQLite), so the images are not yet vulnerability-free and should
  not replace the currently deployed digest without review.
- A reachable `python:3.12-slim-bookworm` candidate was built and scanned as
  `security-20260830-bookworm`; both scans completed with 3 critical, 9 high,
  13 medium, 1 low and 2 undefined findings. It has not been deployed because
  critical/high findings remain.
- In the authenticated production UI, resolving the thumbnail for media
  `ce5ae836-19fa-48e5-850b-490833b74f29` returned the expected full media
  path `/api/media/ce5ae836-19fa-48e5-850b-490833b74f29/content`.

## Open items

- Online verification after the API IAM policy update confirms species search,
  tag search, AND semantics, and reversible bulk tag add/remove. The API role
  now includes the required `dynamodb:BatchWriteItem` permission; the previous
  503/500 failures were caused by that missing action. Query-by-file now
  returns the expected matching record and explicitly reports that the
  temporary query was not archived. DynamoDB remained at four media records
  and the `temporary-query/` S3 prefix was empty after cleanup.
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
- The encrypted remote Terraform backend now reaches the bucket through the
  configured dual-stack regional S3 endpoint. `terraform init -reconfigure`
  succeeds, the default workspace and state are readable, and the live API
  Gateway `$default` stage is imported. A no-refresh plan completed with
  `0 to add, 4 to change, 0 to destroy`; the changes were inspected but not
  applied.
- After the Terraform update, the API Lambda was verified at timeout `300`
  seconds and the production resources were updated in place. The deployment
  variables now pin the API image to the live `repair-20260829` digest
  (`432a229b...`), preventing Terraform from proposing a rollback to the older
  `lambda-20260828-v3` image. A no-refresh plan now reports `No changes`.
- AWS and Alibaba identity checks succeed, and API, Dispatcher and Worker image
  URIs are digest-pinned in the untracked deployment variables.
- The local repository is initialized on `main` and pushed to
  `https://github.com/Friligun/fit5225-a2-pacificbioarchive.git`; GitHub
  currently reports it as public, so an owner must change it to Private and
  invite the teaching team and all members.

## Next actions

1. Capture the remaining live Cognito, upload, processing, thumbnail access,
   query-by-file and deletion evidence listed in `PRE_SUBMISSION_CHECKLIST.md`.
2. Retain the completed 30-image model evaluation and include its 27/30 (90%)
   result and false predictions in the report.
3. Reconcile the four inspected Terraform drifts only after the team reviews
   the saved plan; no resource destruction is proposed.
4. Complete the architecture/demo video and team/individual reports.
