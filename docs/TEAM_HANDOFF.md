# Pacific BioArchive Team Handoff

Updated: 2026-08-28

## Current state

The local application, core API flows, AWS/Alibaba Cloud infrastructure definitions, tests and demo/report templates are present. The system has not yet been deployed and verified end to end in the team's real AWS and Alibaba Cloud accounts. Do not present local demo-mode filename labels as real ML inference.

## Implemented locally

- Auth boundary: production code validates AWS Cognito ID tokens; development uses an isolated demo identity.
- Upload pipeline: SHA-256 deduplication, checksum-bound S3 uploads, SQS dispatch, owner-scoped DynamoDB data and HMAC worker callbacks.
- Worker: Function Compute-compatible image/video processing, thumbnails, one video frame per second, model manifest/versioning and SHA-256 checks.
- User workflows: tag/count AND search, species search, thumbnail resolution, temporary query-by-file, bulk tag edit, deletion and SNS subscriptions.

## Required next actions

1. Create a private Git repository, invite every member and teaching staff, and retain commits from each member.
2. Create an untracked `infra/terraform/terraform.tfvars` using the example values for AWS and Alibaba Cloud.
3. Run Terraform bootstrap with an encrypted remote state backend; build and publish AWS API/dispatcher images to ECR.
4. Deploy the worker image to Alibaba Function Compute. Configure its restricted access, callback secret, worker key and OSS-read permission.
5. Upload supplied `mdv5a.pt` and `model.pt` to private Alibaba OSS at the manifest paths after checking their SHA-256 values.
6. Configure Cognito Hosted UI callback/logout URLs using the deployed API URL, create a test user, verify email and test authentication.
7. Collect real evidence for every workflow in `PRE_SUBMISSION_CHECKLIST.md`, including Function Compute logs and confirmed SNS email.
8. Complete final reports, official AWS/Alibaba architecture diagram, contribution table and required GenAI declarations.

## Important boundaries

- Do not commit `terraform.tfvars`, `.env`, Terraform state, cloud credentials, model weights or test media.
- Keep S3, OSS and the Function Compute worker private. The browser receives only short-lived S3 URLs.
- The Function Compute worker needs the exact shared key and callback HMAC secret produced for the deployed stack.
- External provider login is optional bonus work; do not prioritize it over the required Cognito flow.
