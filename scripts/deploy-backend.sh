#!/bin/bash
set -euo pipefail

APP_DIR="/home/ec2-user/journal-app"
COMPOSE_FILE="docker-compose.dev.yml"

cd "$APP_DIR"

git fetch origin main
git reset --hard origin/main

# .env is created by root during EC2 bootstrap; ec2-user must own it to update
if [ -f .env ]; then
  sudo chown ec2-user:ec2-user .env
  chmod 600 .env
fi

# Ensure production env vars survive git reset (not in repo .env)
ensure_env_var() {
  local key="$1"
  local value="$2"
  if grep -q "^${key}=" .env 2>/dev/null; then
    sed -i "s|^${key}=.*|${key}=${value}|" .env
  else
    echo "${key}=${value}" >> .env
  fi
}

ensure_env_var "ALLOWED_HOSTS" "api.journal-app.a-t-dev.com"
ensure_env_var "CORS_ALLOWED_ORIGINS" "https://journal-app.a-t-dev.com"

/usr/local/bin/docker-compose -f "$COMPOSE_FILE" up -d --build --force-recreate backend

/usr/local/bin/docker-compose -f "$COMPOSE_FILE" exec -T backend python manage.py migrate --noinput

echo "Backend deploy completed successfully."
