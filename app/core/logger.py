import logging
import contextvars

request_id_ctx_var = contextvars.ContextVar("request_id", default="-")

def set_request_id(request_id: str):
    request_id_ctx_var.set(request_id)

def get_request_id() -> str:
    return request_id_ctx_var.get()

# Add request_id to logs
class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = get_request_id()
        return True

# JSON-style structured logs
log_format = '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "request_id": "%(request_id)s"}'

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(log_format))
handler.addFilter(RequestIdFilter())

# Global logger
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
# logger.setLevel(logging.ERROR)
logger.addHandler(handler)