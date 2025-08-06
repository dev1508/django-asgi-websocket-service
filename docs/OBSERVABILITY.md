# Performance & Observability

## 📊 Metrics

We expose Prometheus-compatible metrics at `/metrics` endpoint using `prometheus_client`.

### Exported Metrics:

| Metric Name             | Type     | Description                                      |
|------------------------|----------|--------------------------------------------------|
| `active_connections`   | Gauge    | Number of live WebSocket connections             |
| `total_messages`       | Counter  | Total messages received across all connections   |
| `error_count`          | Counter  | Number of unhandled errors/exceptions            |
| `shutdown_duration`    | Histogram| Time taken during graceful shutdown              |

### Prometheus Scrape Config:

```
- job_name: 'ws-service'
  static_configs:
    - targets: ['localhost:8080']
```

### Example Alert Rules:

```yaml
- alert: NoActiveConnections
  expr: active_connections == 0
  for: 1m
  labels:
    severity: warning
  annotations:
    summary: "No active WebSocket connections for 1 minute"
```

---

## 🩺 Health & Readiness

| Endpoint       | Description                       |
|----------------|-----------------------------------|
| `/healthz`     | Returns `{"status": "ok"}`       |
| `/readyz`      | Returns 200 when app is ready     |

These endpoints are used for container health checks and smoke tests during blue-green deployments.

---

## 📃 Structured Logging

We use structured JSON logs via Python’s `logging` module and `structlog`.

### Example Log:
```json
{
  "timestamp": "2025-08-06 00:33:10",
  "level": "INFO",
  "message": "WebSocket connected",
  "request_id": "344f0b2b-4eb6-4249-9cff-e609cc115c21"
}
```

- Logs include `request_id` for traceability.
- Graceful shutdown, message processing, and exceptions are all logged.

---

## 🔔 Summary

| Feature     | Implemented |
|-------------|-------------|
| `/metrics`  | ✅           |
| `/healthz`  | ✅           |
| `/readyz`   | ✅           |
| Prometheus  | ✅           |
| Alert Rules | ✅           |
| JSON Logs   | ✅           |
| Request IDs | ✅           |

