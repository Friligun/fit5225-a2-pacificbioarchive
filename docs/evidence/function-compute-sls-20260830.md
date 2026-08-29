# Function Compute SLS logging evidence

Captured 2026-08-30 in the Alibaba Cloud `cn-hangzhou` region for function
`pacificbio-worker`.

- SLS logging was enabled after the zero-yuan service activation flow.
- The Function Compute console's `函数日志` view shows the container startup
  messages and live invocation records.
- The records include `FC Invoke Start` and `FC Invoke End` request IDs and
  Uvicorn access lines for `GET /healthz HTTP/1.1` with `200 OK`.
- The screenshot is [28-function-compute-real-logs.png](screenshots-20260830/28-function-compute-real-logs.png).
- Screenshot 16 remains the pre-activation baseline where the console reported
  that logging was not enabled.

The test request used the public HTTP trigger's `/healthz` endpoint and did not
upload, delete, or modify application media.
