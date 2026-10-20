# The base is built from the repository's existing pinned PHP/Node/Composer image.
FROM reclutamiento-sonar-base:local

# PECL upstream, PHP License; 1.0.12 explicitly supports PHP 8.4.
# Quality-only image: does not change the app's runtime or composer.lock.
RUN pecl install pcov-1.0.12 \
    && docker-php-ext-enable pcov

COPY docker/quality/pcov.ini /usr/local/etc/php/conf.d/zz-quality-coverage.ini
