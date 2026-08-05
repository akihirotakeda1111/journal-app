#!/bin/bash
set -euo pipefail

APP_DIR="/home/ec2-user/journal-app"
COMPOSE_FILE="docker-compose.dev.yml"

cd "$APP_DIR"

git fetch origin main
git reset --hard origin/main

/usr/local/bin/docker-compose -f "$COMPOSE_FILE" build backend
/usr/local/bin/docker-compose -f "$COMPOSE_FILE" up -d backend

/usr/local/bin/docker-compose -f "$COMPOSE_FILE" exec -T backend python manage.py migrate --noinput

echo "Backend deploy completed successfully."
