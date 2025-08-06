import os
import django
import asyncio
import json
import datetime

from fastapi import FastAPI

from core.health import router as health_router
from core.instrumentation import instrumentator
from core.metrics import shutdown_duration
from core.request_id_middleware import RequestIDMiddleware

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from chat.routing import websocket_urlpatterns
from chat.consumers import ChatConsumer

from constants.constants import broadcasting_timestamp_duration, process_shutdown_duration

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

heartbeat_task = None

async def broadcast_heartbeat():
    while True:
        await asyncio.sleep(broadcasting_timestamp_duration)
        if len(ChatConsumer.active_connections) == 0:
            print("No Consumers yet")
            continue
        ts = datetime.datetime.utcnow().isoformat()
        print(f"[Heartbeat] Broadcasting to {len(ChatConsumer.active_connections)} clients at {ts}")
        for conn in list(ChatConsumer.active_connections):
            try:
                await conn.send(text_data=json.dumps({"ts": ts}))
            except Exception as e:
                print(f"Failed to send heartbeat: {e}")
                print(f"[Heartbeat Error] {e} — removing {repr(conn)}")
                ChatConsumer.active_connections.discard(conn)

async def lifespan(scope, receive, send):
    global heartbeat_task
    while True:
        message = await receive()
        if message["type"] == "lifespan.startup":
            heartbeat_task = asyncio.create_task(broadcast_heartbeat())
            await send({"type": "lifespan.startup.complete"})
        elif message["type"] == "lifespan.shutdown":
            print("[Shutdown] Initiated. Closing all WebSocket connections...")
            with shutdown_duration.time():
                if heartbeat_task:
                    heartbeat_task.cancel()
                    try:
                        await heartbeat_task
                    except asyncio.CancelledError:
                        print("[Shutdown] Heartbeat task cancelled.")

                shutdown_deadline = asyncio.create_task(asyncio.sleep(process_shutdown_duration))
                print(f"shutdown_deadline - {shutdown_deadline}")

                connections_snapshot = list(ChatConsumer.active_connections)
                print(f"[Shutdown] Attempting to close {len(connections_snapshot)} active connections...")

                close_tasks = [
                    conn.close(code=1001)
                    for conn in list(ChatConsumer.active_connections)
                ]
                print(f"close_tasks - {close_tasks}")

                done, pending = await asyncio.wait(
                    close_tasks + [shutdown_deadline],
                    return_when=asyncio.FIRST_COMPLETED,
                )

                print(f"[Shutdown] Gracefully closed {len(close_tasks)} connections (or they were already closed).")
                print(f"[Shutdown] Closed {len(close_tasks)} connections.")

            await send({"type": "lifespan.shutdown.complete"})
            break


fastapi_app = FastAPI()
fastapi_app.add_middleware(RequestIDMiddleware)
fastapi_app.include_router(health_router)
instrumentator.instrument(fastapi_app).expose(fastapi_app)

application = ProtocolTypeRouter({
    "http": fastapi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
    "lifespan": lifespan,
})