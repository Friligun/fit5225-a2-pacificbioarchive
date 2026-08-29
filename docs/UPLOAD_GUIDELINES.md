# Pacific BioArchive Code Upload Guidelines

This document standardizes how the four code packages are prepared and
uploaded for FIT5225 Assignment 2. It applies to source-code packages, not to
production media uploads.

## Package layout

Each member owns one responsibility package based on the final committed
snapshot (`7315f27`). Use these exact filenames:

| Package | Responsibility |
| --- | --- |
| `01-api-auth-persistence.zip` | API routes, Cognito authentication, schemas and data persistence |
| `02-media-frontend-workflow.zip` | Browser UI, media helpers, search workflow and user-facing tests |
| `03-ml-worker-video.zip` | Function Compute worker, model assets metadata and video processing |
| `04-infrastructure-deployment.zip` | Terraform, Lambda dispatcher, deployment scripts and cloud evidence |

## Branch and commit rules

- Create one branch per package using `member-<number>-<responsibility>`.
- Keep package `01` on `member-01-api-auth-persistence`, and use the same
  pattern for packages `02` through `04`.
- Start each branch from the current `main` branch. Do not force-push or
  rewrite another member's branch.
- Upload one ZIP per branch and use a descriptive commit message, for example:
  `Add member 01 API auth persistence package`.
- Keep the original 12-commit project history unchanged. Package divisions are
  responsibility bundles for review and reporting, not fabricated authorship.

## Contents and exclusions

Each ZIP must contain the assigned source files, related tests, and the
configuration or documentation needed to understand that responsibility. Do
not include:

- `.env`, access keys, passwords, JWTs, API tokens or presigned URLs;
- `terraform.tfvars`, Terraform state files, plan files or `.terraform/`;
- model weight binaries, private cloud credentials or local databases;
- `.git/`, virtual environments, caches, `__pycache__/`, uploads or temporary
  runtime output.

## Pre-upload checks

1. Confirm the ZIP opens and contains only the assigned package scope.
2. Run `git diff --check` and the local test/preflight checks before the final
   upload.
3. Compute a SHA-256 checksum with
   `Get-FileHash <package>.zip -Algorithm SHA256` and retain it for the report.
4. Verify the branch name and commit message before pushing.
5. After pushing, open the branch on GitHub and confirm the ZIP, commit author,
   timestamp and file size are visible.

## Reporting rule

Use the package responsibility as a starting point for the individual report,
but describe only work that the member actually reviewed, understood and can
explain. The package split must not be presented as evidence that a member
authored commits they did not make.
