# Cognito evidence screenshots

Captured 2026-08-30 for the first live-evidence item:

1. `01-unauthorized-api-media.png` - anonymous GET /api/media returns Unauthorized.
2. `02-cognito-confirmation.png` - Cognito confirmation page showing the masked email and verification form.
3. `03-authenticated-home.png` - authenticated project home showing the user email and `Sign out`.
4. `04-signed-out-home.png` - project home after logout showing `Sign in required` and `Sign in`.
5. `05-multi-select-before-tags.png` - four media records selected together before a bulk tag operation.
6. `06-bulk-add-tags-focus.png` - bulk `Add tags` result; `evidence-bulk-20260830` appears on all selected media.
7. `07-bulk-remove-tags-focus.png` - bulk `Remove tags` result; the temporary evidence tag is absent from all media.
8. `08-and-query.png` - AND tag query `bos_taurus:1, felis_catus:1`; only `Bos_taurus_1.JPG` is returned and both matching tags are visible.
9. `09-single-species-query.png` - single-species query `felis_catus`; the two matching image records are returned.
10. `10-thumbnail-preview.png` - thumbnail URL resolution for the `Felis_catus_3.JPG` thumbnail; the page reports the corresponding full media URL.
11. `11-video-ready-and-tags.png` - authenticated species query page showing the processed video search context.
12. `12-video-ready-card.png` - `alectura_lathami` query returning `video.mp4` and an image; the video is `ready` with model-generated tags.
13. `13-dynamodb-media-items.png` - AWS DynamoDB item explorer showing the current media records, including `video.mp4`.
14. `14-s3-raw-before-delete.png` - AWS S3 `raw/` media prefix baseline.
15. `15-s3-thumbnails-before-delete.png` - AWS S3 `thumbnails/` media prefix baseline.
16. `16-function-compute-logs-disabled.png` - Alibaba Function Compute logging page showing that SLS logging is not enabled and may incur charges when enabled.
17. `17-dynamodb-delete-before.png` - DynamoDB before-delete baseline containing the test media record.
18. `18-s3-test-before-delete.png` - S3 raw source object before deletion.
19. `19-s3-test-thumbnail-before-delete.png` - S3 thumbnail object before deletion.
20. `20-app-test-delete-complete.png` - Application confirmation after deleting the selected test media.
21. `21-s3-test-after-delete-raw.png` - S3 raw prefix after deletion, showing no objects.
22. `22-s3-test-after-delete-thumbnail.png` - S3 thumbnail prefix after deletion, showing no objects.
23. `23-dynamodb-test-after-delete.png` - DynamoDB after-delete scan showing 44 items and no test record.
24. `24-test-media-restored.png` - Application after re-upload, showing the restored test image as `ready`.
25. `25-s3-test-restored-raw.png` - Restored S3 raw source object.
26. `26-s3-test-restored-thumbnail.png` - Restored S3 thumbnail object.
27. `27-dynamodb-test-restored.png` - DynamoDB after restoration containing the test record again.
28. `28-function-compute-real-logs.png` - Alibaba Function Compute SLS function-log view showing container startup, FC invoke start/end request IDs, and successful `/healthz` 200 responses.

The temporary tag `evidence-bulk-20260830` was removed after the evidence capture.
The `06-bulk-add-tags.png` and `07-bulk-remove-tags.png` files are full-page
captures; the corresponding `*-focus.png` files are the clearer media-card
captures for report use.

No password or verification code is included in these screenshots. Keep the
original mailbox screenshot with the code out of the submission bundle, or
redact the code before using it.
