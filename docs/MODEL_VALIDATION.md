# Model Validation Procedure

The supplied `model.pt` and `mdv5a.pt` assets are checksum-pinned in `models/model-manifest.json`. The Worker verifies those values before loading the trusted supplied classifier with legacy PyTorch deserialization.

## Current validation status

The supplied model files are restored at `models/model.pt` and `models/mdv5a.pt`,
and all 30 supplied fixture images are available under
`tests/fixtures/test_images/`. Their manifest checksums pass. Do not substitute
fabricated assets: the assessment demonstration requires the supplied files.

The local automated suite verifies artifact integrity and fixture coverage. A
separate real-model evaluation over all 30 labelled images is recorded in
`tmp/model-evaluation-summary.json` and currently reports **27/30 correct
(90%)**. The three observed false predictions are retained in that file and
must be disclosed in the report rather than inferred away from filenames.

Run the following only after worker dependencies have installed:

```powershell
.\.venv\Scripts\python.exe scripts\run_model_smoke.py
```

`worker/requirements.txt` includes the pinned `onnx2torch` dependency required
by the supplied model path. The worker image was rebuilt successfully with the
current pins and deployed to Alibaba Function Compute.

Expected evidence to retain for the report/demo:

1. Command output showing the active model version and non-error prediction result.
2. Model SHA-256 values matching the manifest.
3. Alibaba Function Compute log for the same test asset or a production upload.
4. The compact accuracy table over the 30 supplied labelled test images from
   `tmp/model-evaluation-summary.json`. Report actual results, including all
   false predictions; do not infer correctness from filenames.

The separate local UI's `demo_filename` mode is for API/UI workflow only and is explicitly not acceptable evidence of ML inference.
