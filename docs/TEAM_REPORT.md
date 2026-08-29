# Pacific BioArchive: Team Report

**Unit:** FIT5225 Assignment 2  
**Repository:** [03xf/FIT5225-Assessment-2](https://github.com/03xf/FIT5225-Assessment-2) (private repository; teaching staff must be invited before submission)

## 1. System overview and design choices

Pacific BioArchive is an authenticated, multi-cloud wildlife-media archive. AWS provides Cognito, API Gateway, Lambda, S3, DynamoDB, SQS and SNS. Alibaba Cloud provides a private Function Compute worker and protected OSS model artifacts. This split keeps identity, durable metadata and user-facing APIs in AWS while placing the supplied, dependency-heavy MegaDetector/SpeciesNet runtime in a service suited to a large container. Uploads are asynchronous through SQS, so the API remains responsive; query-by-file is synchronous and has a 300-second API timeout to accommodate worker cold start. Private object storage and short-lived signed URLs reduce exposure, while the additional cloud boundary demonstrates portability and controlled trust between providers.

## 2. Multi-cloud architecture

The final architecture figure should use the official AWS and Alibaba Cloud service icons and show this flow:

```text
Browser -> Cognito Hosted UI -> API Gateway (JWT) -> API Lambda
                         |             |-- DynamoDB owner metadata/tag index
                         |             |-- private S3 raw + thumbnail objects
                         |             `-- SQS -> dispatcher Lambda
                         |                           -> signed request -> Alibaba FC worker
                         |                                                  |-> private OSS models
                         |                                                  `-> HMAC callback -> API Lambda -> DynamoDB/SNS
```

The browser calculates SHA-256 and receives no long-lived cloud credentials or worker URL. API Gateway rejects unauthenticated `/api/*` requests. Lambda roles are scoped to required prefixes and services; the worker requires a dispatcher-only shared key and signs callbacks with HMAC. The complete trust-boundary description is in [ARCHITECTURE.md](ARCHITECTURE.md).

## 3. Functional implementation and testing guide

1. Open the deployed UI at `https://7ijuyi2q17.execute-api.ap-southeast-2.amazonaws.com/`, register and verify a Cognito account, then demonstrate sign-in, sign-out and anonymous `/api/media` rejection (HTTP 401).
2. Upload `Bos_taurus_1.JPG`. The browser computes SHA-256, a checksum-bound presigned S3 PUT is completed, and DynamoDB records the owner-scoped item. Uploading the identical file again returns the existing media ID without a second object or item.
3. Upload the supplied `video.mp4`. The worker samples one frame per second, creates an aspect-preserving thumbnail, verifies the manifest-pinned model hashes, and writes aggregate tags. The record reached `READY` with model version `supplied-2026-08`; live FC evidence is in [function-compute-sls-20260830.md](evidence/function-compute-sls-20260830.md).
4. Run a single-species search and an AND query such as `felis_catus:1, bos_taurus:1`; only records satisfying every term and minimum count are returned. Resolve a thumbnail URL while authenticated and repeat as another user to demonstrate owner isolation.
5. Submit an image through query-by-file. Results are returned from a TTL-bound temporary prefix; no media item is added and the temporary object is removed after processing.
6. Select multiple records, add and remove a temporary tag, then delete a selected test record. Verify both S3 source/thumbnail prefixes and the DynamoDB item before and after; re-upload the test image only after the evidence capture.
7. Subscribe to `felis_catus`, confirm the SNS email, and upload/tag matching media. The notification screenshot and all workflow screenshots are indexed in [evidence/README.md](evidence/README.md).

## 4. Evidence and limitations

The deployed AWS region is `ap-southeast-2`; the Alibaba region is `cn-hangzhou`; the worker is `pacificbio-worker`. The local regression suite passes **16 tests**. Evidence includes Cognito authentication, anonymous rejection, checksum deduplication, video readiness, AND/species queries, thumbnail ownership, query-by-file cleanup, bulk tags, deletion/restoration, SNS confirmation, storage/database state and real SLS invocation logs. The current image scan still reports upstream base-layer vulnerabilities (`CRITICAL=4` and `HIGH` findings), so the final submission must either rebuild on remediated bases or record an explicit, justified risk decision. The SQS DLQ also contains three historical failed messages and should be reviewed before the final recording. No accuracy percentage is claimed because a measured 30-image evaluation has not been completed.

## 5. Team contributions

| Name and student ID | Contribution % | Delivered work |
|---|---:|---|
| **[Member 1 name] ([student ID])** | **[ ]%** | API contracts, Cognito/JWT authentication, owner-scoped media and DynamoDB persistence; commits are visible in the private repository. |
| **[Member 2 name] ([student ID])** | **[ ]%** | Terraform AWS/Alibaba infrastructure, SQS dispatcher, Function Compute worker integration and deployment evidence. |
| **[Member 3 name] ([student ID])** | **[ ]%** | Browser UI, upload/checksum flow, search, bulk tag and deletion workflows, and live test evidence. |
| **[Member 4 name] ([student ID], if applicable)** | **[ ]%** | Model validation, security testing, documentation and report/evidence integration. |

Replace bracketed identity and percentage fields with the team's truthful allocation. The percentages must comply with the assignment rule and total 100%; every listed member must have a visible repository contribution.

## 6. Generative AI declaration

GPT was used only to brainstorm design options and to help debug implementation errors. Team members reviewed every suggestion, tested the resulting system, and can explain, modify and defend the submitted code and architecture.
