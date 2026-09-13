#!/bin/sh
# Prepares a fresh or existing checkout and starts the given command (app and app-e2e services).
set -e

cd /var/www/html

# APP_ENV=e2e makes Laravel load .env.e2e (isolated E2E database and Redis databases).
if [ "${APP_ENV:-}" = "e2e" ]; then
    ENV_FILE=.env.e2e
    [ -f "$ENV_FILE" ] || sh docker/php/init-e2e-env.sh
else
    ENV_FILE=.env
    [ -f "$ENV_FILE" ] || cp .env.example "$ENV_FILE"
fi

if [ ! -f vendor/autoload.php ]; then
    composer install --no-interaction --prefer-dist
fi

if ! grep -q '^APP_KEY=base64:' "$ENV_FILE"; then
    php artisan key:generate --force
fi

if [ ! -x node_modules/.bin/vp ]; then
    npm ci --no-audit --no-fund
fi

if [ ! -f public/build/manifest.json ]; then
    npm run build
fi

mkdir -p storage/app/private storage/framework/cache/data storage/framework/sessions storage/framework/views storage/logs bootstrap/cache

php artisan migrate --force

if [ "${SEED_ON_BOOT:-false}" = "true" ]; then
    php artisan db:seed --force
fi

exec "$@"
