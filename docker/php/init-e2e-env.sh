#!/bin/sh
# Creates .env.e2e from .env.e2e.example with a random APP_KEY and E2E_TOKEN (values are never printed).
set -e

cd /var/www/html

if [ -f .env.e2e ]; then
    echo ".env.e2e ya existe; no se modifica."
    exit 0
fi

cp .env.e2e.example .env.e2e

KEY=$(php -r 'echo "base64:".base64_encode(random_bytes(32));')
TOKEN=$(php -r 'echo bin2hex(random_bytes(32));')

sed -i "s|^APP_KEY=.*|APP_KEY=${KEY}|; s|^E2E_TOKEN=.*|E2E_TOKEN=${TOKEN}|" .env.e2e

echo ".env.e2e creado con APP_KEY y E2E_TOKEN generados (no se muestran)."
