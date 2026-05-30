#!/bin/bash
set -e

DOMAIN="api.journal-app.a-t-dev.com"
EMAIL="akihirotakeda1111@gmail.com"
YML_FILE="docker-compose.dev.yml"
APP_PATH="/home/ec2-user/journal-app"

cp $APP_PATH/nginx/http.conf.template $APP_PATH/nginx/default.conf
docker-compose -f $YML_FILE up -d nginx backend

docker-compose -f $YML_FILE run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d $DOMAIN --email $EMAIL --agree-tos --no-eff-email

cp $APP_PATH/nginx/https.conf.template $APP_PATH/nginx/default.conf
docker-compose -f $YML_FILE restart nginx