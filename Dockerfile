FROM python:3.9-slim

# Set base directory
WORKDIR /app/app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app code
COPY ./app /app/app

# Set PYTHONPATH so 'core' can be resolved
ENV PYTHONPATH=/app/app

# CMD to run app with concurrency tuning
#
# Explanation:
# - Using 2 workers for parallelism (sufficient for local/dev testing)
# - uvloop for high-perf event loop (ideal for I/O-bound async apps)
# - Our Django app is ASGI-capable via Channels
#   so it's able to handle thousands of concurrent socket connections
#
CMD ["uvicorn", "core.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--loop", "uvloop"]