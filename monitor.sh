#!/bin/bash

METRICS_URL="http://localhost:8000/metrics"
LOG_FILE="logs.txt"

echo "[Monitor] Starting log/error and metrics monitoring"
echo "[Monitor] Watching $LOG_FILE for 'ERROR' lines..."
echo "[Monitor] Polling $METRICS_URL every 10 seconds..."

# Tail logs for "ERROR" (in background)
tail -F "$LOG_FILE" | grep --line-buffered "ERROR" &
TAIL_PID=$!

# Extract top-5 counters from /metrics every 10s
while true; do
  echo -e "\n[Monitor] Fetching metrics at $(date):"
  curl -s "$METRICS_URL" \
    | grep '^ws_.* [0-9]' \
    | sort -k2 -nr \
    | head -n 5
  sleep 10
done

# Ensure tail process is killed on script exit
trap "kill $TAIL_PID" EXIT