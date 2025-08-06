from starlette.middleware.base import BaseHTTPMiddleware
import uuid
from core.logger import set_request_id

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        rid = str(uuid.uuid4())
        set_request_id(rid)
        response = await call_next(request)
        return response