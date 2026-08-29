# Live upload evidence — 2026-08-29

This evidence bundle records the authenticated production upload flow. Secrets,
session tokens and S3 signatures are intentionally redacted.

## 1. Browser SHA-256

| Asset | SHA-256 | Result |
|---|---|---|
| `Bos_taurus_1.JPG` (fixture used for the live image workflow) | `9f0f9f5cb5f0d51aa8c07540a1e9cbbf3100c3bd7ac9d2fe007af937c1dd2bf7` | matches metadata and duplicate record |
| `query-test.jpg` (temporary upload/delete test) | `9f0f9f5cb5f0d51aa8c07540a1e9cbbf3100c3bd7ac9d2fe007af937c1dd2bf7` | upload/delete workflow verified |
| `video.mp4` | `7ea7541da1db313a6550a086dfa78d1d7002d96e5ed4a7e995a12d040800c97f` | video workflow reached `READY` |

The image hash was also sent as the `x-amz-meta-sha256` value and browser upload
checksum. The duplicate upload returned the original media record rather than
creating a second object.

## 2. Short-lived S3 upload URL

The browser received HTTP 200 from `POST /api/upload-sessions`, then issued a
signed `PUT` to the following redacted URL:

```text
https://pacific-bioarchive-9d14dd8f.s3.amazonaws.com/raw/<owner-sub>/<media-id>/source.jpg
  ?content-type=image/jpeg
  &x-amz-checksum-sha256=nw+fXLXw1RqowHVAoenLvzEAw716ydL+AHr5N8HdK/c=
  &x-amz-meta-sha256=9f0f9f5cb5f0d51aa8c07540a1e9cbbf3100c3bd7ac9d2fe007af937c1dd2bf7
  &Expires=1788005596
  &AWSAccessKeyId=<redacted>&Signature=<redacted>&x-amz-security-token=<redacted>
```

The observed S3 response status was `200`. The URL was valid only for the
short expiry window and is not retained as a credential.

## 3. DynamoDB record

The production image record used for the duplicate/processing evidence is:

```text
media_id: ce5ae836-19fa-48e5-850b-490833b74f29
filename: Bos_taurus_1.JPG
entity: media
status: READY
checksum_sha256: 9f0f9f5cb5f0d51aa8c07540a1e9cbbf3100c3bd7ac9d2fe007af937c1dd2bf7
```

The production video record is `66d273fd-edba-4628-a9a1-78882d943191`; it
reached `READY` with a generated thumbnail, aggregate frame tags and model
version `supplied-2026-08`. The temporary test record
`80c8da15-2c96-46f6-b862-c93333ffb626` was deleted and is documented in
`test-media-deletion.txt`.

## 4. Thumbnail evidence

The image pipeline generates a compressed, aspect-ratio-preserving thumbnail.
The video pipeline samples `video.mp4` at `fps=1` (16 frames at timestamps
0–15 seconds) and stores the generated thumbnail path in the video DynamoDB
record. Frame/timestamp evidence is in `video-fps1.txt`; the production record
and thumbnail-path result are described in `CLOUD_EVIDENCE_20260828.md`.

## 5. Function Compute logs and model version

Function Compute worker: `pacificbio-worker`.

* health check returned HTTP 200 after the 180-second startup allowance;
* the video callback completed with status `READY`;
* callback model version: `supplied-2026-08`;
* video frame filter: `fps=1,showinfo`;
* model manifest: `models/model-manifest.json`.

Manifest SHA-256 values:

```text
mdv5a.pt  fe3e90e4b1955821ab7c1f88b446dc0c8cb25e109fdd1872916a55305294a5ef
model.pt  dfc99bd1e0c8b14c6755f4504460c414f678e72936d5f849f9947dff84ca913a
```

The corresponding implementation and deployment notes are in
`MODEL_VALIDATION.md`, `IMPLEMENTATION_STATUS.md`, and
`CLOUD_EVIDENCE_20260828.md`.
