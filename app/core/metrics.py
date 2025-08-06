from prometheus_client import Counter, Gauge, Summary

total_messages = Counter("ws_total_messages", "Total messages received via WebSocket")
active_connections = Gauge("ws_active_connections", "Number of active WebSocket connections")
error_count = Counter("ws_error_count", "Total WebSocket errors")
shutdown_duration = Summary("ws_shutdown_duration_seconds", "Time taken to shutdown gracefully")