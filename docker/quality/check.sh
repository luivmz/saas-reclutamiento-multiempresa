#!/bin/sh
set -eu
cd /var/www/html

# Laravel's test bootstrap expects the local template to exist, as in CI.
# Runtime test credentials and APP_KEY still come from the isolated container.
if [ ! -f .env ]; then
    cp .env.example .env
fi

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
        # Direct PHPUnit avoids Collision adding a second --configuration option.
        php vendor/bin/phpunit --configuration=.quality/phpunit.xml --testdox --coverage-clover=coverage.xml --log-junit=test-results.xml
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
