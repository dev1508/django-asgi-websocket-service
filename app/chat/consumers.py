import json
import uuid

from channels.generic.websocket import AsyncWebsocketConsumer
from core.metrics import total_messages, active_connections, error_count
from core.logger import logger, set_request_id, get_request_id

class ChatConsumer(AsyncWebsocketConsumer):
    session_store: dict[str, int] = {}
    active_connections = set()

    async def connect(self):
        rid = str(uuid.uuid4())
        set_request_id(rid)

        # 🔁 Get session_id from query string
        self.session_id = self.scope['query_string'].decode()
        self.session_id = self.session_id.replace("session_id=", "") if self.session_id else str(uuid.uuid4())

        logger.info(f"Session Id: {self.session_id}")

        # 🔁 Resume counter if session_id exists
        self.counter = ChatConsumer.session_store.get(self.session_id, 0)


        ChatConsumer.active_connections.add(self)
        active_connections.inc()

        logger.info("WebSocket connected", extra={"request_id": get_request_id()})
        logger.info(f"Total active connections: {len(ChatConsumer.active_connections)}",
                    extra={"request_id": get_request_id()})
        await self.accept()

    async def disconnect(self, close_code):
        rid = str(uuid.uuid4())
        set_request_id(rid)

        ChatConsumer.active_connections.discard(self)
        active_connections.dec()

        logger.info("WebSocket disconnected", extra={"request_id": get_request_id()})
        logger.info(f"Remaining connections: {len(ChatConsumer.active_connections)}",
                    extra={"request_id": get_request_id()})

    async def receive(self, text_data=None, bytes_data=None):
        rid = str(uuid.uuid4())
        set_request_id(rid)

        try:
            total_messages.inc()
            if text_data == "quit":
                logger.info("Client requested shutdown", extra={"request_id": get_request_id()})
                await self.send(text_data=json.dumps({
                    'bye': True,
                    'total': self.counter
                }))
                await self.close(code=1000, reason="quit command received")
            else:
                self.counter += 1
                ChatConsumer.session_store[self.session_id] = self.counter
                logger.info(f"Received message {self.counter}: {text_data}",
                            extra={"request_id": get_request_id()})

                await self.send(text_data=json.dumps({
                    'count': self.counter
                }))
        except Exception as e:
            # logger.error(f"Error received: {e}, for {text_data}", extra={"request_id": req_id})
            error_count.inc()
            raise e