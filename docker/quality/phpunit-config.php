<?php

// Derive from the canonical configuration, preserving forced testing settings.
// Absolute paths prevent the .quality/ location from changing test discovery.
$root = dirname(__DIR__, 2);
$document = new DOMDocument;
$document->load($root.'/phpunit.xml');
$xpath = new DOMXPath($document);
$document->documentElement->setAttribute('bootstrap', $root.'/vendor/autoload.php');
foreach ($xpath->query('/phpunit/testsuites/testsuite/directory') as $directory) {
    $directory->nodeValue = $root.'/'.$directory->nodeValue;
}
$include = $xpath->query('/phpunit/source/include')->item(0);
while ($include->firstChild !== null) {
    $include->removeChild($include->firstChild);
}
foreach (['app', 'routes', 'resources', 'database', 'config', 'bootstrap', 'public'] as $path) {
    $directory = $document->createElement('directory', $root.'/'.$path);
    $directory->setAttribute('suffix', '.php');
    $include->appendChild($directory);
}
$exclude = $document->createElement('exclude');
foreach (['bootstrap/cache', 'public/build', 'public/storage'] as $path) {
    $exclude->appendChild($document->createElement('directory', $root.'/'.$path));
}
$xpath->query('/phpunit/source')->item(0)->appendChild($exclude);
$document->formatOutput = true;
if (! is_dir($root.'/.quality')) {
    mkdir($root.'/.quality', 0700, true);
}
$document->save($root.'/.quality/phpunit.xml');
