#!/bin/sh
set -e

cd /var/www/html

[ -f .env ] || cp .env.example .env

if [ ! -f vendor/autoload.php ]; then
    composer install --no-interaction --prefer-dist
fi

if ! grep -q '^APP_KEY=base64:' .env; then
    php artisan key:generate --force
fi

if [ ! -x node_modules/.bin/vp ]; then
    npm ci --no-audit --no-fund
fi

if [ ! -f public/build/manifest.json ]; then
    npm run build
fi

php artisan migrate --force

if [ "${SEED_ON_BOOT:-false}" = "true" ]; then
    php artisan db:seed --force
fi

exec "$@"
