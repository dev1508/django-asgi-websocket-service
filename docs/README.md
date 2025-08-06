# Django ASGI WebSocket Service

A high-performance Django + ASGI WebSocket service with full observability, blue-green deployments, graceful shutdown, and reconnection support.

## Technologies Used

- **Django**
- **Docker** 
- **Prometheus**
- **Grafana**
- **Nginx**

## Tools Required

To run and test the project, you may take help of the following tools:

- **PyCharm**
- **Terminal**

---

## 🚀 One-liner to Spin Up Full Stack

```bash
docker-compose down -v && docker-compose build && docker-compose up
```

This will:

- Build and run `app_blue`, `app_green`, and `nginx`
- Expose the live app on `http://localhost:8080`

---

## 📈 Load Testing

This service supports WebSocket load testing using a simple Python script (`ws_load_test.py`).

### 🔁 Run WebSocket Load Test

```bash
cd <project-root-level>
python ws_load_test.py
```

This simulates 5000 concurrent sockets sending and receiving messages via `/ws/chat/`.

A sample set of logs of the load test can be found at - [testing_logs/load_test_logs.txt](https://github.com/dev1508/django-asgi-websocket-service/blob/main/testing_logs/load_test_logs.txt). 


---

## 🔁 Blue-Green Deployment

The app supports seamless blue-green deployments via Nginx reverse proxy.

### 🔄 Promote New Version

```bash
./promote.sh
```

This script:

1. Detects currently live version (blue or green)
2. Builds and runs the other version
3. Runs a smoke test via `/healthz`
4. Switches traffic via `nginx/default.conf`
5. Gracefully stops the old version

---

## 📦 Project Structure

```bash
service/
├── app/               # Django app
├── nginx/             # Nginx reverse proxy config
├── grafana/           # Grafana Dashboard JSON
├── prometheus/        # Prometheus Alert Rules
├── promote.sh         # Blue-green switch script
├── monitor.sh         # Monitors prometheus metrics
├── testing_files      # Test scripts
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## ✅ Functional Summary

- **WebSocket**: `/ws/chat/` receives text and replies with counter
- **Graceful shutdown**: Handles SIGTERM, exits cleanly
- **Reconnection**: Optional query param `?session_id=...` resumes counter
- **Server Push**: Heartbeat every 30s
- **Observability**: `/metrics`, `/healthz`, `/readyz`, logs, alerts
- **Performance**: Supports 5K+ concurrent sockets with <3s startup, <10s shutdown

---

For more details, refer to `DESIGN.md` and `OBSERVABILITY.md`.

---

Happy Hacking ⚡

