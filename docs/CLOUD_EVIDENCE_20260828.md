# Cloud Deployment Evidence (2026-08-28)

This record contains non-secret deployment evidence. Access keys, shared keys,
callback secrets, model weights and Terraform state are intentionally omitted.

## AWS

- Account: `748998941962`
- Region: `ap-southeast-2`
- API Gateway: `https://7ijuyi2q17.execute-api.ap-southeast-2.amazonaws.com`
- `GET /api/health`: HTTP 200, `{"status":"ok","environment":"production"}`
- `GET /auth/config`: HTTP 200 with the deployed Cognito client and domain
- Cognito callback/logout URLs: deployed API HTTPS origin
- API Gateway `$default` stage: auto-deploy enabled
- API and Dispatcher Lambda image URIs are digest-pinned in the untracked
  `infra/terraform/terraform.tfvars`.

## Alibaba Cloud

- Region: `cn-hangzhou`
- Function: `pacificbio-worker`
- Public HTTP trigger: `https://pacifico-worker-gcddpyefvh.cn-hangzhou.fcapp.run`
- Worker image: public ECR digest-pinned image, without model weights or secrets
- RAM execution role: `PacificBioWorkerOssReadRole`
- Role policy: `AliyunOSSReadOnlyAccess`
- Model bucket: `pacificbio-models-748998941962-20260828`
- `GET /healthz`: HTTP 200, CPU mode and manifest path reported
- `/process` without `x-worker-key`: HTTP 401 (`Worker authentication failed`)

## Local verification

- Python test suite: `16 passed`
- Changes were pushed to GitHub commits `6315665` and `d558cc0`.

## Online regression (2026-08-29)

- Authenticated production UI showed the Cognito user `2273264790@qq.com`.
- Species search for `bos_taurus` returned `Bos_taurus_1.JPG`.
- Tag search for `bos_taurus:1` returned the same media record.
- AND search for `codex-regression:1, bos_taurus:1` returned only the target
  record after a temporary tag was added.
- The temporary tag was removed successfully; the original model tag set was
  restored.
- SNS email subscription for `felis_catus` was confirmed from the AWS email;
  the topic now reports one confirmed subscription and no pending
  confirmations. Screenshot evidence: `docs/evidence/sns-subscription-confirmed.png`.
- CloudWatch identified the earlier API 503/500 responses as a missing
  `dynamodb:BatchWriteItem` permission. The API role policy was updated and
  the regression passed afterward.
- `scripts/preflight.ps1` completed successfully: 16 Python tests passed,
  Terraform validation passed, and Docker reported server version `29.7.2`.
- Unauthenticated `GET /api/media` returned HTTP `401`.
- ECR vulnerability scans for the API and Dispatcher image digests completed.
  The current scan evidence is recorded in
  `docs/evidence/model-deployment-evidence-20260829.md`; it reports
  `CRITICAL=4, HIGH=15, MEDIUM=6, LOW=1, UNDEFINED=2` for each digest and must
  be remediated or explicitly risk-accepted before submission.
- Authenticated thumbnail resolution for media `ce5ae836-19fa-48e5-850b-490833b74f29`
  returned `/api/media/ce5ae836-19fa-48e5-850b-490833b74f29/content`.
- A fresh authenticated query-by-file attempt with
  `tests/fixtures/test_images/Bos_taurus_1.JPG` returned HTTP `503`; this is
  recorded as a deployed query-service outage, not as a passing match result.
- A direct Worker `/healthz` check from the deployment workstation timed out,
  corroborating that the query failure is in the Worker/network path.

## Recheck (2026-08-29)

- Public `GET /api/health` returned HTTP `200` with the production status.
- Unauthenticated `GET /api/media` returned HTTP `401` as expected.
- The browser reached production mode and showed an authenticated Cognito
  session, but the authenticated media-list request still returned HTTP `401`.
  No upload, tag mutation or deletion was attempted during this recheck.

## Authenticated regression continuation (2026-08-29)

- After re-authentication, the production UI identified user
  `2273264790@qq.com` and loaded the existing media records.
- A temporary `felis_catus` tag was added successfully to
  `Bos_taurus_1.JPG`; the UI reported `Tags added.`.
- Tag search for `felis_catus:1, bos_taurus:1` returned only the target media,
  confirming logical AND semantics.
- `Felis_catus_3.JPG` was uploaded through the authenticated production UI,
  reached `READY`, and was classified with `felis_catus x 1`.
- The QQ mailbox received an AWS SNS email with subject
  `Pacific BioArchive: felis_catus detected` and payload event `tag-added` for
  media `fab0d0c8-8d38-4e0f-a9f3-e0af0ac55d4d`, confirming the live notification
  path. The temporary tag on `Bos_taurus_1.JPG` was left unchanged pending an
  explicit cleanup request.
- After signing in again, a duplicate upload of `Bos_taurus_1.JPG` returned
  `Ready: Bos_taurus_1.JPG`. The archive still contained exactly the original
  three media records, and the existing `Bos_taurus_1.JPG` media ID
  `ce5ae836-19fa-48e5-850b-490833b74f29` was unchanged. This verifies
  checksum-based duplicate handling without creating a second media item.
- The supplied `video.mp4` was uploaded successfully and created media ID
  `66d273fd-edba-4628-a9a1-78882d943191`. After approximately four minutes,
  the production UI initially reported `video | processing | not classified`.
  The Alibaba Function Compute health check was then extended to allow the
  large worker image 180 seconds to start. The existing record subsequently
  reached `READY` without a duplicate upload; its DynamoDB item contains the
  generated thumbnail path, model version `supplied-2026-08`, and aggregate
  tags for `alectura_lathami`, `casuarius_casuarius`,
  `chalcophaps_longirostris`, `dacelo_novaeguineae`,
  `gymnorhina_tibicen`, `hypsiprymnodon_moschatus`, `megapodius_reinwardt`
  and `rattus_rattus`.

## Worker startup repair (2026-08-29)

- Function Compute `pacificbio-worker` kept its digest-pinned image, 8192 MB,
  4 vCPU, 900-second timeout, port 8080, execution role and environment.
- Only `customContainerConfig.healthCheckConfig` changed: initial delay 180s,
  period 30s, timeout 10s, failure threshold 6, success threshold 1.
- Public `GET /healthz` then returned HTTP 200 with the CPU device and model
  manifest path, and the previously uploaded video completed processing.

## Query-by-file repair and verification (2026-08-29)

- CloudWatch showed the API Lambda query request timing out at 30 seconds
  while waiting for the remote worker. The API Lambda timeout was increased to
  300 seconds; its memory, image and environment were unchanged.
- After re-authentication, query-by-file with `Bos_taurus_1.JPG` returned the
  existing `Bos_taurus_1.JPG` match and the UI reported:
  `Temporary query processed; it was not archived.`
- DynamoDB still contained four `entity=media` records before and after the
  query. The scoped S3 `temporary-query/` prefix contained five stale objects
  from the earlier forced timeouts; those temporary objects were removed and
  a follow-up list returned no contents. No raw media or thumbnails were
  deleted.

## Second Cognito user setup (2026-08-29)

- The previously unconfirmed `ypei0023@student.monash.edu` account was
  recreated and successfully authenticated in the production UI.
- Its archive is empty, while the original user's four media records remain
  intact. The original thumbnail path was entered in the ownership resolver and
  the UI returned `Thumbnail URL is not owned by this user`; no full-media URL
  was returned for the second user. The second user's archive remained empty.

## Queue and DLQ check (2026-08-29)

- The processing SQS source queue is enabled with batch size 1 and a redrive
  policy of `maxReceiveCount=3` to the dedicated processing DLQ.
- The source queue currently has 0 visible and 0 in-flight messages.
- The DLQ has 3 older failed messages from the previous worker outage. They
  were not replayed or deleted; review them before final submission if a clean
  DLQ screenshot is required.

## Outstanding evidence

- Register and verify a real Cognito user, then capture the authenticated
  upload, processing, deletion and SNS workflows.
- Capture Function Compute logs and a real model-processing callback.
- Import the API Gateway stage into Terraform state when the S3 backend endpoint
  is reachable from the local Terraform client. The stage is already live in AWS.
- Terraform `init -reconfigure -input=false` initially timed out because the
  default regional hostname resolved to an unreachable address. The backend
  now uses `https://s3.dualstack.ap-southeast-2.amazonaws.com`; subsequent init,
  workspace listing and state reads succeeded. The live API Gateway `$default`
  stage was imported as `aws_apigatewayv2_stage.default`. A no-refresh plan
  completed with `0 to add, 4 to change, 0 to destroy`; it was inspected and
  not applied.
