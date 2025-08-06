#!/bin/bash

set -e

# Extract current active app from nginx/default.conf
ACTIVE_APP=$(grep 'server app_.*:8000;' ./nginx/default.conf | grep -v '^ *#' | awk '{print $2}' | cut -d':' -f1)

if [ "$ACTIVE_APP" == "app_blue" ]; then
    echo "🟢 app_blue is live. Deploying 🟢app_green..."
    TARGET="app_green"
    OLD="app_blue"
else
    echo "🟢 app_green is live. Deploying 🟢app_blue..."
    TARGET="app_blue"
    OLD="app_green"
fi

echo "🔄 Building and starting $TARGET..."
docker-compose -f docker-compose.yml up -d --build $TARGET

echo "🧪 Running smoke test..."
sleep 5
curl --fail http://localhost:8080/healthz || {
    echo "❌ Smoke test failed!"
    docker-compose -f docker-compose.yml stop $TARGET
    exit 1
}

echo "✅ Smoke test passed. Switching traffic..."

echo "🔧 Updating Nginx config to point to $TARGET..."

# Update nginx/default.conf dynamically
if [ "$TARGET" == "app_blue" ]; then
    sed -i '' 's/^    server app_green:8000;/    # server app_green:8000;/' ./nginx/default.conf
    sed -i '' 's/^    # server app_blue:8000;/    server app_blue:8000;/' ./nginx/default.conf
else
    sed -i '' 's/^    server app_blue:8000;/    # server app_blue:8000;/' ./nginx/default.conf
    sed -i '' 's/^    # server app_green:8000;/    server app_green:8000;/' ./nginx/default.conf
fi

# Reload nginx container to apply changes
NGINX_CONTAINER=$(docker ps --filter "name=nginx" --format "{{.Names}}" | head -n 1)
docker exec "$NGINX_CONTAINER" nginx -s reload
# docker exec sigiq-ws-service-nginx-1 nginx -s reload

echo "🟢 $TARGET is now handling traffic via Nginx"

echo "🧹 Stopping old version: $OLD"
docker-compose -f docker-compose.yml stop $OLD

echo "🎉 Blue-Green deployment complete. $TARGET is now live."