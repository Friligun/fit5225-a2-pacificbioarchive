# Individual Report: Zhihao Qian

**Student ID:** 36667625  
**Team:** Group 13  
**Assigned area:** Member 03 - ML worker and video processing

## Role and contribution

I was responsible for the ML worker and video-processing area. I maintained the separate Alibaba Function Compute service boundary so the large model runtime is not placed inside the ordinary API Lambda. The worker authenticates dispatcher requests with a shared key, downloads a short-lived input URL, verifies checksum-pinned detector and classifier assets from the model manifest, and returns results through an HMAC-signed callback. For images it runs detection and classification, creates a compressed thumbnail and reports aggregate species tags. For videos it uses FFmpeg to sample one frame per second, processes the sampled frames and creates a thumbnail from the first frame. I helped diagnose the initial worker cold-start problem and verified the repaired Function Compute health check, `READY` video record, generated tags and live SLS logs. The model version, hashes, video evidence and Function Compute log screenshot are indexed under `docs/evidence`.

I kept model artifacts outside the container image and used an immutable manifest to identify the active detector and classifier. At runtime the worker checks each downloaded file's SHA-256 before deserializing it, which prevents an accidental or tampered replacement from being used. The callback payload carries the media owner, model version and normalized tags, allowing the API to update one deterministic record. These choices support the rubric's model-integrity, video-processing and cross-cloud security requirements.

## Teamwork reflection

The worker had the strongest dependency on the other parts of the system: it needed valid signed URLs from the dispatcher, a callback contract from the API and model artifacts available through Alibaba OSS. The team handled this well by testing `/healthz` separately before attempting a full media request. That isolated startup and network failures from model failures and made the final diagnosis faster. I also learned that a technically correct container can still look broken when its health-check window is too short for a large image. The handover would have been better with an earlier written cold-start budget and a small synthetic worker request, rather than discovering the timing issue during the live video test.

The live SLS records were especially valuable because they showed the difference between container startup, Function Compute invocation and application access logs. I would improve the process by adding a repeatable smoke request to the deployment runbook and by measuring cold-start duration before setting the health-check delay. That would make future model updates easier to validate without waiting for a full media upload.

## Generative AI declaration

GPT was used only to brainstorm design options and to help debug implementation errors. I reviewed every suggestion, tested the resulting system, and can explain, modify and defend my submitted work.
