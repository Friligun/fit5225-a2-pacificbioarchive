# Two-Phase Deployment Runbook

This runbook intentionally separates infrastructure bootstrap from application
release. Use a team-owned AWS account and Alibaba Cloud account; do not put credentials,
model weights or Terraform state in Git.

## 1. Bootstrap infrastructure

1. Copy `infra/terraform/terraform.tfvars.example` to an untracked
   `terraform.tfvars` and set the Alibaba region/bucket, AWS account ID and unique
   Cognito domain prefix.
2. Configure an encrypted remote Terraform backend before the first apply.
3. Run `terraform init`, `terraform plan` and then `terraform apply` with all
   three image URI variables empty. This creates the private ECR repositories,
   Alibaba OSS model bucket and AWS data-plane resources.
4. Record `api_ecr_repository_url`, `dispatcher_ecr_repository_url`,
   `alibaba_oss_model_bucket` and `api_gateway_url` from `terraform output`.

## 2. Publish immutable images and model assets

Build and push the API and dispatcher images to AWS ECR. Deploy the worker
image to Alibaba Function Compute using `Dockerfile.worker` and configure its
private HTTP endpoint in `alibaba_processor_url`.

Upload the supplied model objects to the returned private Alibaba OSS bucket, retaining
the manifest paths exactly:

```text
oss://<alibaba_oss_model_bucket>/models/mdv5a.pt
oss://<alibaba_oss_model_bucket>/models/model.pt
```

Before upload, compare both SHA-256 values with `models/model-manifest.json`.
The Function Compute execution role has object-read access only.

## 3. Deploy and configure login

1. Set the three image digest URIs in `terraform.tfvars` and apply again.
2. Replace `ui_callback_urls` and `ui_logout_urls` with the HTTPS
   `api_gateway_url` output (plus a trailing slash if required by the Hosted
   UI), then apply once more.
3. Open the API URL, use Cognito Hosted UI to register with first name, last
   name, verified email and password, then validate sign-in and sign-out.
4. Complete an SNS subscription from the application and retain its
   confirmation email for the demo.

## 4. Release gates

- Run `terraform validate`, all Python tests and the real
  `scripts/run_model_smoke.py` before presenting.
- Verify Function Compute is private, the worker can only be invoked through
  the dispatcher shared key, and no cloud credential is committed.
- Follow [PRE_SUBMISSION_CHECKLIST.md](PRE_SUBMISSION_CHECKLIST.md) to capture
  the required evidence.
