# Deployment Inputs and Decisions

This checklist contains no credentials. Keep actual values in untracked `infra/terraform/terraform.tfvars` and in cloud secret/environment settings.

## Confirm before creating cloud resources

| Input | Recommended value | Why it is needed |
|---|---|---|
| AWS account ID | `748998941962` | Terraform restricts the deployment identity and names AWS resources. |
| AWS region | `ap-southeast-2` or another single chosen AWS region | Cognito, API Gateway, Lambda, S3, DynamoDB, SQS and SNS should be deployed together. |
| Alibaba region | `cn-hangzhou` | Used for the private OSS model bucket and Function Compute worker. |
| Alibaba OSS bucket | Globally unique lowercase name, for example `pacificbio-models-<team>-<random>` | Private storage for `models/mdv5a.pt` and `models/model.pt`. |
| Cognito domain prefix | Globally unique lowercase prefix | Required for Hosted UI sign-up/sign-in. |
| API and dispatcher image digests | Immutable ECR image URIs after bootstrap | Required to create AWS Lambda image functions. |
| Worker image | Immutable Alibaba Container Registry image URI | Required to deploy the Function Compute worker container. |
| Function Compute endpoint | Private/internal endpoint reachable from the AWS dispatcher | Passed to the dispatcher and API configuration. |
| Final UI URL | API Gateway HTTPS URL | Required for the Cognito callback and logout URLs. |

## Worker configuration

Set these only in Function Compute configuration or an approved secret service, never in Git:

- `WORKER_SHARED_KEY`: must match the stack's `PACIFICBIO_WORKER_SHARED_KEY`.
- `CALLBACK_HMAC_SECRET`: must match `PACIFICBIO_WORKER_CALLBACK_HMAC_SECRET`.
- `ALIBABA_OSS_BUCKET`, `ALIBABA_OSS_ENDPOINT`, `ALIBABA_CLOUD_REGION` and `ALIBABA_MODEL_PREFIX=models`.
- Use a least-privilege RAM role or short-lived credentials limited to `GetObject` on the model bucket's `models/*` prefix.

## Required supplied files

Restore these assessment files before local validation and before uploading models:

- `models/mdv5a.pt`
- `models/model.pt`
- 30 supplied images under `tests/fixtures/test_images/`
- At least one supplied or team-owned short video for the one-frame-per-second demonstration

## Cloud actions that create billable resources

- AWS: ECR, Lambda, API Gateway, S3, DynamoDB, SQS, SNS and CloudWatch logs.
- Alibaba Cloud: OSS, Container Registry storage/transfer if used, Function Compute execution and logs.

Review the Terraform plan and the Function Compute deployment configuration before applying them. AWS credits cannot pay Alibaba Cloud charges.
