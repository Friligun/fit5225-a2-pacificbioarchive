# Submission Readiness Checklist

Use this only with evidence from the team's own deployment. A checked box is a claim you can demonstrate live, not merely a feature found in source code.

## Before cloud apply

- [ ] Put the AWS account ID, Alibaba Cloud region/bucket, unique Cognito domain prefix, image URIs, Function Compute endpoint and final UI origin in an untracked `terraform.tfvars`.
- [x] Use an encrypted remote Terraform state backend and inspect `terraform plan` with all team members. The S3 backend is encrypted and reachable through the configured dual-stack regional endpoint; `terraform init -reconfigure`, workspace listing and state reads now succeed. A no-refresh plan reported `0 to add, 4 to change, 0 to destroy`; it was inspected but not applied.
- [ ] Confirm AWS permits the selected region/services and Alibaba Cloud billing, OSS and Function Compute are enabled.
- [ ] Build and scan API, dispatcher and worker images; push API/dispatcher images to private ECR and deploy the worker image to Function Compute. API/Dispatcher `security-20260829-v2` scans are `COMPLETE` but still report 4 critical and 8 high findings from the upstream Python/Debian base layer; further base-image remediation or a documented risk decision is required.
- [ ] Upload the supplied model files only to protected Alibaba OSS, and verify the manifest hashes before deployment.

## Required live evidence

- [ ] Register a new email/password user in Cognito Hosted UI, verify email, sign in, sign out, and show anonymous `/api/*` rejection.
- [ ] Upload an image; show browser SHA-256, short-lived S3 upload, DynamoDB record, compressed aspect-preserving thumbnail, Function Compute log and model version. **Evidence bundle added:** `docs/evidence/upload-evidence-20260829.md`; direct console-log and thumbnail screenshots remain to be captured before final recording.
- [x] Upload the identical image again and show it returns the first media record without a second object or metadata item. Verified on 2026-08-29 with `Bos_taurus_1.JPG`; the archive remained at three records and preserved media ID `ce5ae836-19fa-48e5-850b-490833b74f29`.
- [x] Upload a video; the supplied `video.mp4` reached `READY` after the Function Compute health-check startup window was extended. DynamoDB now contains the generated thumbnail path, model version `supplied-2026-08`, and aggregate frame tags; capture the frame/timestamp screenshot for the final evidence bundle.
- [ ] Search with two `species:minimum` terms and show logical AND; then search a single species.
- [x] Resolve a thumbnail URL to the full media URL while signed in, and show a different Cognito user cannot retrieve it. With `ypei0023@student.monash.edu` signed in, the original user's thumbnail returned `Thumbnail URL is not owned by this user`; the second user's archive remained empty.
- [x] Use query-by-file and show it returns matches but no new media/table item; inspect the temporary prefix after completion. Verified after the API timeout repair: the UI returned `Bos_taurus_1.JPG`, reported that the temporary query was not archived, DynamoDB remained at four media records, and `temporary-query/` was empty after cleanup.
- [ ] Select multiple records, add tags with operation `1`, remove them with operation `0`, and delete selected media. Show S3 and DynamoDB before/after.
- [ ] Subscribe to a tag, confirm the SNS email, upload/tag matching media and show the received notification.
- [ ] Show the private Function Compute access boundary, scoped Alibaba RAM/OSS policy, SQS/DLQ and the absence of cloud credentials in source control. Current SQS source queue is enabled with `maxReceiveCount=3`; the DLQ currently contains 3 old failed messages and should be reviewed/cleared only with explicit approval.

## Assessment artifacts

- [ ] Prepare a 3-minute architecture overview using official AWS/Alibaba Cloud icons, then rehearse the 15-minute functional demo with every member speaking.
- [ ] Replace all report placeholders, keep team report <=1000 words and each individual report <=500 words.
- [ ] Include the required selective-GenAI acknowledgement in both reports, with only truthful usage.
- [ ] Make the repository private, invite the teaching staff, and confirm every member's commits/contribution table are visible.
- [ ] Preserve screenshots, CloudWatch/Function Compute logs, commands, model version/hash and test output in the evidence folder before submission. Hashes, redacted presigned URL metadata, model version and test output are indexed in `docs/evidence/README.md`.
- [ ] Run `./scripts/preflight.ps1` immediately before the final recording; use `-RunModelSmoke` once Worker dependencies are available.
- [ ] Build the three local containers and invoke the API/Dispatcher Lambda runtime smoke paths before pushing immutable image digests.
