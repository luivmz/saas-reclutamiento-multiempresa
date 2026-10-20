#!/bin/sh
set -eu
cd /var/www/html

# Install the locked versions. Do not run the project's composer setup/reset scripts.
if [ ! -f vendor/autoload.php ] || [ "$(cat vendor/.quality-lock 2>/dev/null || true)" != "$(sha256sum composer.lock | cut -d ' ' -f 1)" ]; then
    composer install --no-interaction --prefer-dist --no-progress
    sha256sum composer.lock | cut -d ' ' -f 1 > vendor/.quality-lock
fi
mkdir -p storage/framework/cache/data storage/framework/sessions storage/framework/views storage/logs bootstrap/cache

case "${1:-tests}" in
    tests)
        # Same sources as the scan's PHP scope. No exclusion of uncovered authored PHP.
        php docker/quality/phpunit-config.php
        php artisan test --configuration=.quality/phpunit.xml --coverage-clover=coverage.xml --log-junit=test-results.xml
        test -s coverage.xml
        test -s test-results.xml
        ;;
    frontend)
        npm ci --no-audit --no-fund
        npm run build
        npx --no-install tsc --noEmit
        npx --no-install vp test --run
        ;;
    *) echo 'Use tests or frontend.' >&2; exit 2 ;;
esac
