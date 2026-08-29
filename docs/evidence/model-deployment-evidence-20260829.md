# Model and image deployment evidence — 2026-08-29

## Model manifest

```text
active_version: supplied-2026-08
mdv5a.pt SHA-256: fe3e90e4b1955821ab7c1f88b446dc0c8cb25e109fdd1872916a55305294a5ef
model.pt SHA-256: dfc99bd1e0c8b14c6755f4504460c414f678e72936d5f849f9947dff84ca913a
```

The manifest is `models/model-manifest.json`; model weights remain excluded
from source control. The production video record reached `READY` with model
version `supplied-2026-08` and one-frame-per-second processing evidence.

## Immutable image references

```text
API        pacific-bioarchive-api-9d14dd8f:security-20260829-v2@sha256:d91158cfac3f2cc5f82e16bec3e83edf6e0efecd39e5a0c1427723d708b40923
Dispatcher pacific-bioarchive-dispatcher-9d14dd8f:security-20260829-v2@sha256:c996046c35b45f94b3f621259b330791f0e3c999f9457428ef021677c3e35776
```

The API security rebuild upgrades the Debian system packages during image
construction. Its ECR scan completed with `CRITICAL=4, HIGH=8, MEDIUM=5,
LOW=1`; the remaining findings are in upstream system packages and still need
remediation or explicit risk acceptance before submission. The Dispatcher
security image was pushed as a single manifest; ECR's per-image scan quota was
already exhausted when a new scan was requested, so no new Dispatcher counts
are claimed here.

## Function Compute evidence

Historical production evidence records worker health check HTTP 200, the
180-second startup allowance, video callback status `READY`, generated
thumbnail path and model version `supplied-2026-08`. Capture a current
Function Compute log screenshot for the final demo if the console is available.
