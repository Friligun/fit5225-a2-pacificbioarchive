# Evidence index

| Requirement | Evidence |
|---|---|
| Browser SHA-256 and short-lived S3 upload | [upload-evidence-20260829.md](upload-evidence-20260829.md) |
| DynamoDB media fields and model callback | [upload-evidence-20260829.md](upload-evidence-20260829.md), [CLOUD_EVIDENCE_20260828.md](../CLOUD_EVIDENCE_20260828.md) |
| Video frame sampling | [video-fps1.txt](video-fps1.txt) |
| Model manifest hashes/version | [model-hashes-20260829.txt](model-hashes-20260829.txt), [MODEL_VALIDATION.md](../MODEL_VALIDATION.md) |
| Upload/delete UI state | [test-media-deleted.png](test-media-deleted.png), [test-media-deletion.txt](test-media-deletion.txt) |
| SNS subscription and actual watched-tag notification | [sns-subscription-confirmed.png](sns-subscription-confirmed.png) (subscription confirmation), [sns-tag-added-notification-20260829.png](sns-tag-added-notification-20260829.png) (actual `felis_catus` `tag-added` notification) |
| Query and bulk-management contracts | [query-bulk-evidence-20260829.md](query-bulk-evidence-20260829.md) |
| Bulk tag selection, add/remove success, and ignored missing-tag removal | [screenshots-20260830/06-bulk-select.png](screenshots-20260830/06-bulk-select.png), [screenshots-20260830/07-bulk-add-tags-success.png](screenshots-20260830/07-bulk-add-tags-success.png), [screenshots-20260830/07-bulk-remove-tags-success.png](screenshots-20260830/07-bulk-remove-tags-success.png), [screenshots-20260830/07-bulk-remove-missing-tag.png](screenshots-20260830/07-bulk-remove-missing-tag.png) |
| Authenticated species query and processed video state | [screenshots-20260830/12-video-ready-card.png](screenshots-20260830/12-video-ready-card.png) |
| AWS media-state baseline | [screenshots-20260830/13-dynamodb-media-items.png](screenshots-20260830/13-dynamodb-media-items.png), [screenshots-20260830/14-s3-raw-before-delete.png](screenshots-20260830/14-s3-raw-before-delete.png), [screenshots-20260830/15-s3-thumbnails-before-delete.png](screenshots-20260830/15-s3-thumbnails-before-delete.png) |
| Alibaba Function Compute logging status and real invocation logs | [function-compute-sls-20260830.md](function-compute-sls-20260830.md), [screenshots-20260830/16-function-compute-logs-disabled.png](screenshots-20260830/16-function-compute-logs-disabled.png) (before), [screenshots-20260830/28-function-compute-real-logs.png](screenshots-20260830/28-function-compute-real-logs.png) (SLS enabled with live logs) |
| Test-media deletion and restoration | [test-media-delete-restore-20260830.txt](test-media-delete-restore-20260830.txt), [screenshots-20260830/17-dynamodb-delete-before.png](screenshots-20260830/17-dynamodb-delete-before.png), [screenshots-20260830/18-s3-test-before-delete.png](screenshots-20260830/18-s3-test-before-delete.png), [screenshots-20260830/19-s3-test-thumbnail-before-delete.png](screenshots-20260830/19-s3-test-thumbnail-before-delete.png), [screenshots-20260830/20-app-test-delete-complete.png](screenshots-20260830/20-app-test-delete-complete.png), [screenshots-20260830/21-s3-test-after-delete-raw.png](screenshots-20260830/21-s3-test-after-delete-raw.png), [screenshots-20260830/22-s3-test-after-delete-thumbnail.png](screenshots-20260830/22-s3-test-after-delete-thumbnail.png), [screenshots-20260830/23-dynamodb-test-after-delete.png](screenshots-20260830/23-dynamodb-test-after-delete.png), [screenshots-20260830/24-test-media-restored.png](screenshots-20260830/24-test-media-restored.png), [screenshots-20260830/25-s3-test-restored-raw.png](screenshots-20260830/25-s3-test-restored-raw.png), [screenshots-20260830/26-s3-test-restored-thumbnail.png](screenshots-20260830/26-s3-test-restored-thumbnail.png), [screenshots-20260830/27-dynamodb-test-restored.png](screenshots-20260830/27-dynamodb-test-restored.png) |
| AWS/Alibaba security controls | [cloud-security-evidence-20260829.md](cloud-security-evidence-20260829.md) |
| Model and image deployment | [model-deployment-evidence-20260829.md](model-deployment-evidence-20260829.md) |
| Multi-cloud architecture | [architecture-diagram.svg](architecture-diagram.svg), [../TEAM_REPORT.md](../TEAM_REPORT.md) |
| AWS IAM, SQS/DLQ and Alibaba OSS private ACL | [screenshots-20260830/29-aws-iam-policy.png](screenshots-20260830/29-aws-iam-policy.png), [screenshots-20260830/30-aws-sqs-dlq-configuration.png](screenshots-20260830/30-aws-sqs-dlq-configuration.png), [screenshots-20260830/31-aws-sqs-redrive-settings.png](screenshots-20260830/31-aws-sqs-redrive-settings.png), [screenshots-20260830/32-alibaba-oss-private-acl.png](screenshots-20260830/32-alibaba-oss-private-acl.png) |
| Core functional UI evidence | [screenshots-20260830/10-thumbnail-preview.png](screenshots-20260830/10-thumbnail-preview.png) (thumbnail/query-by-file controls), [screenshots-20260830/09-single-species-query.png](screenshots-20260830/09-single-species-query.png) (single-species search), [screenshots-20260830/11-video-ready-and-tags.png](screenshots-20260830/11-video-ready-and-tags.png) (video READY/tags), [screenshots-20260830/18-s3-test-before-delete.png](screenshots-20260830/18-s3-test-before-delete.png) and [screenshots-20260830/21-s3-test-after-delete-raw.png](screenshots-20260830/21-s3-test-after-delete-raw.png) (S3 deletion before/after) |
| Checksum validation | [screenshots-20260830/03-authenticated-home.png](screenshots-20260830/03-authenticated-home.png) (authenticated checksum-validated archive banner), [upload-evidence-20260829.md](upload-evidence-20260829.md) (SHA-256 and duplicate-upload result) |

The S3 URL in the upload record is intentionally redacted to remove temporary
credentials and signatures. The AWS media-state baseline, completed
deletion/restoration evidence, and Function Compute logging transition are
captured in
`screenshots-20260830/13-dynamodb-media-items.png`,
`screenshots-20260830/14-s3-raw-before-delete.png`,
`screenshots-20260830/15-s3-thumbnails-before-delete.png`, and
`screenshots-20260830/16-function-compute-logs-disabled.png` and
`screenshots-20260830/28-function-compute-real-logs.png`. The textual
production record is already preserved in `CLOUD_EVIDENCE_20260828.md`.
