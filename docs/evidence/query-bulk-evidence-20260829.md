# Query and bulk-management evidence — 2026-08-29

## Query behaviour

The production regression record in `CLOUD_EVIDENCE_20260828.md` documents:

* `bos_taurus:1` species/count search returning `Bos_taurus_1.JPG`;
* `felis_catus:1, bos_taurus:1` returning only the intersection record;
* single-species search for `bos_taurus` returning the same record;
* thumbnail resolution returning the owner-scoped full media URL;
* query-by-file returning a match while leaving DynamoDB unchanged and the
  `temporary-query/` S3 prefix empty after cleanup.

The local API regression suite also covers the same contracts:

```text
tests/test_api.py -k "tag or species or delete or bulk or query"
3 passed, 3 deselected in 3.83s
```

## Bulk tag and delete contract

The API contract is implemented at `POST /api/media/tags`:

```json
{"media_ids":["<id-1>","<id-2>"],"tags":["demo-tag"],"operation":1}
{"media_ids":["<id-1>","<id-2>"],"tags":["demo-tag"],"operation":0}
```

Operation `1` adds the tag to every selected owner-scoped record. Operation `0`
removes only the requested tag and ignores tags that are not present. The
existing automated test suite verifies bulk add/remove and deletion. The live
UI evidence to capture before recording is one screenshot showing multiple
selected cards, the `Tags added.` and `Tags removed.` statuses, followed by
before/after S3 and DynamoDB views for deletion. The completed test-media
deletion and restoration sequence is documented in
`test-media-delete-restore-20260830.txt` with screenshots 17-27 in the
`screenshots-20260830/` directory. The original single test-media delete proof
is also retained in `test-media-deleted.png` and `test-media-deletion.txt`.

The authenticated species-query screenshot
`screenshots-20260830/12-video-ready-card.png` shows `alectura_lathami`
matching both the processed `video.mp4` record and an image record. The video
card is `ready` and displays the model-generated species/count tags.
