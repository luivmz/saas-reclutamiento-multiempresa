<?php

$proxies = array_filter(array_map(trim(...), explode(',', (string) env('TRUSTED_PROXIES', ''))), static function (string $entry): bool {
    [$ip, $prefix] = array_pad(explode('/', $entry, 2), 2, null);

    if (filter_var($ip, FILTER_VALIDATE_IP) === false) {
        return false;
    }

    if ($prefix === null) {
        return true;
    }

    return filter_var($prefix, FILTER_VALIDATE_INT, [
        'options' => ['min_range' => 1, 'max_range' => str_contains($ip, ':') ? 128 : 32],
    ]) !== false;
});

return [
    'proxies' => array_values($proxies),
];
