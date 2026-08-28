# Cloud Deployment Evidence (2026-08-28)

This record contains non-secret deployment evidence. Access keys, shared keys,
callback secrets, model weights and Terraform state are intentionally omitted.

## AWS

- Account: `748998941962`
- Region: `ap-southeast-2`
- API Gateway: `https://7ijuyi2q17.execute-api.ap-southeast-2.amazonaws.com`
- `GET /api/health`: HTTP 200, `{"status":"ok","environment":"production"}`
- `GET /auth/config`: HTTP 200 with the deployed Cognito client and domain
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

## Outstanding evidence

- Register and verify a real Cognito user, then demonstrate the authenticated
  upload, processing, search, bulk-tag, deletion and SNS workflows.
- Capture Function Compute logs and a real model-processing callback.
- Import the API Gateway stage into Terraform state when the S3 backend endpoint
  is reachable from the local Terraform client. The stage is already live in AWS.
