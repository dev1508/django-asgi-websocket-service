# Design discussion

## ⚙️ ASGI & Concurrency Design

This WebSocket service is built using **Django Channels**, running on **Uvicorn** ASGI server, and is designed for high concurrency with minimal overhead.

---

## 🧵 Workers vs Thread Pool

### Uvicorn Workers:

We run multiple ASGI workers to utilize all CPU cores and achieve concurrency:

```bash
uvicorn core.asgi:application --host 0.0.0.0 --port 8000 --workers 2 --loop uvloop
```

- `--workers 2`: One worker per CPU core (adjustable based on hardware).
- `--loop uvloop`: High-performance event loop built on libuv (great for I/O-bound tasks).

### Why ASGI Workers?

- ASGI workers are **processes**, not threads, and provide **true parallelism**.
- Each worker handles thousands of concurrent WebSocket connections via the event loop.

### Django Thread Pool:

Thread pools are **not used** explicitly here. We avoid long blocking I/O calls inside consumers to prevent blocking the event loop. Any future I/O-heavy or CPU-bound work should be offloaded to Celery/RQ or a separate worker service.

---

## 🛑 No Shared Mutable State

We strictly avoid shared mutable state between connections or workers:

- WebSocket counter is stored **per connection**.
- Session data (`session_store`) is maintained **in-memory** inside each ASGI worker.
  - This means it will not persist across workers or restarts (intentional for assignment scope).
- No cross-request globals are used.

---

## 🔁 Session Resume via Query Param

Reconnecting clients can send `?session_id=...` in query params. The in-memory session store resumes their previous counter.

```python
self.session_id = self.scope['query_string'].decode().replace("session_id=", "")
self.counter = ChatConsumer.session_store.get(self.session_id, 0)
```

This is safe because each ASGI worker handles its own connections and does not share session memory.

---

## 💡 Summary

| Topic          | Design                                 |
| -------------- | -------------------------------------- |
| ASGI Server    | Uvicorn + uvloop                       |
| Concurrency    | Multiple workers via `--workers`       |
| Loop           | `uvloop` for async event handling      |
| Thread Pools   | Avoided, not used                      |
| Shared State   | Avoided, session scoped per connection |
| Resume Support | `session_id` param in URL              |

This design ensures safe, scalable concurrency while staying true to ASGI principles.

