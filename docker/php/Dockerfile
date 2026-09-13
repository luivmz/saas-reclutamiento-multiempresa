# Development/demo image for the Laravel app and the queue worker. Versions are pinned for reproducible builds
# (see docs/docker.md). Source code, vendor/ and node_modules/ are mounted at runtime by docker-compose.yml.
ARG PHP_VERSION=8.4.25
ARG NODE_VERSION=22.23.2
ARG COMPOSER_VERSION=2.10.3

FROM composer:${COMPOSER_VERSION} AS composer
FROM node:${NODE_VERSION}-bookworm-slim AS node

FROM php:${PHP_VERSION}-cli-bookworm AS base

ARG PHPREDIS_VERSION=6.3.0

RUN apt-get update \
    && apt-get install -y --no-install-recommends git unzip libpq-dev libzip-dev libicu-dev curl \
    && docker-php-ext-install pdo_pgsql pgsql zip intl bcmath pcntl opcache \
    && pecl install "redis-${PHPREDIS_VERSION}" \
    && docker-php-ext-enable redis \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=composer /usr/bin/composer /usr/bin/composer
COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
    && ln -s /usr/local/lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx

COPY docker/php/php.ini /usr/local/etc/php/conf.d/zz-app.ini

WORKDIR /var/www/html

ENV PHP_CLI_SERVER_WORKERS=4

EXPOSE 8000

CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8000"]
