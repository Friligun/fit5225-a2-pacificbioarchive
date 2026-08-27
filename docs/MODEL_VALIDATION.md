# Model Validation Procedure

The supplied `model.pt` and `mdv5a.pt` assets are checksum-pinned in `models/model-manifest.json`. The Worker verifies those values before loading the trusted supplied classifier with legacy PyTorch deserialization.

## Current local blocker

This checkout does not contain the supplied model files or the 30 supplied fixture images. Restore them to `models/model.pt`, `models/mdv5a.pt` and `tests/fixtures/test_images/` before running the checks below. Do not substitute fabricated assets: the manifest hash checks and the assessment demonstration require the supplied files.

The local automated suite also verifies the manifest hashes of both supplied
assets and confirms the 30 provided fixture images cover 13 filename-labelled
species. This proves artifact integrity, not model prediction accuracy.

Run the following only after worker dependencies have installed:

```powershell
.\.venv\Scripts\python.exe scripts\run_model_smoke.py
```

`worker/requirements.txt` intentionally does not include `onnx2torch`: the
worker calls MegaDetector directly and never imports it. Keeping it out avoids
an unnecessary source-build dependency during the reproducible worker image
build.

Expected evidence to retain for the report/demo:

1. Command output showing the active model version and non-error prediction result.
2. Model SHA-256 values matching the manifest.
3. Alibaba Function Compute log for the same test asset or a production upload.
4. A compact accuracy table over the 30 supplied labelled test images. Report actual results, including any false predictions; do not infer correctness from filenames.

The separate local UI's `demo_filename` mode is for API/UI workflow only and is explicitly not acceptable evidence of ML inference.
