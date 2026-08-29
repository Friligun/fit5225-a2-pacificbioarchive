# Cloud security evidence — 2026-08-29

## AWS controls

* Unauthenticated `GET /api/media` returned HTTP `401`.
* S3 media bucket CORS allows `PUT` only from the deployed HTTPS UI origin and
  only the content/checksum headers required by the upload flow.
* The API IAM policy is scoped to `raw/*`, `thumbnails/*` and `temporary-query/*`
  plus the media table/index, processing queue and notification topic. It
  includes only the required DynamoDB batch/transaction actions and SNS
  publish/subscribe actions.
* SQS source queue attributes: SSE enabled, visibility timeout 900 seconds,
  redrive `maxReceiveCount=3`, 0 visible messages and 0 in-flight messages at
  capture time. The dedicated DLQ contains 3 older failed messages and was not
  modified.
* The repository `.gitignore` excludes `.env`, Terraform variables/state,
  model weights and local uploads. No credentials are included in this evidence
  bundle.

## Alibaba Cloud controls

Terraform configuration creates the model OSS bucket with versioning enabled
and `alicloud_oss_bucket_acl.models.acl = "private"`. The worker reads models
through the internal OSS endpoint and rejects requests without `x-worker-key`
with HTTP `401` (historical production evidence in
`CLOUD_EVIDENCE_20260828.md`). A fresh probe from the deployment workstation on
2026-08-29 timed out, so no new live success claim is made here.

## Remaining screenshot

Before final recording, capture the AWS IAM policy, SQS/DLQ attributes and
Alibaba RAM/OSS private ACL in the consoles. Do not include access keys, worker
shared keys or signed URLs in screenshots.
