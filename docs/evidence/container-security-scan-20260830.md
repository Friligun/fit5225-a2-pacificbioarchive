# Container security scan (2026-08-30)

## Scope

AWS ECR enhanced/basic image scans were queried for the immutable API and
Dispatcher digests published as `security-20260829-v2`. Both scans returned
`COMPLETE` with the same counts: **4 CRITICAL, 8 HIGH, 5 MEDIUM, 1 LOW**.
The counts are findings in the upstream `python:3.12-slim` Debian layer; they
are not evidence that the application was exploited.

## What the high/critical findings mean

- `glibc` issues can cause memory corruption when an exposed process reaches a
  vulnerable parsing path. The API does not expose a raw `scanf` interface, so
  exploitability depends on a vulnerable library call being reachable through
  a request or dependency.
- `perl` Socket/regex issues can permit memory disclosure, denial of service,
  or incorrect matching when those Perl APIs are called with attacker input.
  Perl is not part of the API/Dispatcher application path; it is inherited as
  an OS package.
- `sqlite3` FTS5 issues require a crafted SQLite database and an FTS5 query;
  the service uses DynamoDB for metadata and does not accept SQLite databases.
- OpenSSL findings affect specific CMS/CMP code paths. TLS termination is
  provided by API Gateway, and the application does not process CMS/CMP
  messages.

The practical residual risk is therefore primarily supply-chain/compliance
risk and denial-of-service risk if a future feature invokes an affected path,
rather than a demonstrated remote compromise of the current endpoints.

## Mitigations applied

1. API and Dispatcher Dockerfiles run `apt-get upgrade` during image build and
   remove the apt cache.
2. Worker Dockerfile now performs the same upgrade before installing ffmpeg and
   libgl1.
3. Images are immutable digest-pinned; the currently deployed Lambda digest was
   not replaced without a clean scan and runtime verification.
4. API Gateway JWT authorization, private S3/OSS storage, scoped IAM/RAM
   policies, and HMAC worker callbacks limit reachable attack surface.

The reachable Bookworm candidate was built and pushed for scan as:

- API: `sha256:3fe3315732e14a7ff046f61fa65b0dd7cead3e6e10b2d8baa0f5dc58f115e22b`
- Dispatcher: `sha256:b576142dd80061504a37d8071e9b730844d810f146511e6d57288fec58319ff8`

Its scan completed with **3 critical, 9 high, 13 medium, 1 low and 2
undefined** findings. This is an improvement over the prior 4/8/5/1 result,
but it is still not a zero-finding release and has not been deployed.

The AWS Lambda public base image could not be pulled on this network (CloudFront
EOF), so migration to that base image was not verified. The reachable
`python:3.12-slim-bookworm` candidate was scanned successfully, but remains an
un-deployed candidate because critical/high findings remain.
