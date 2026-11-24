<?php

namespace Tests\Feature\Frontend;

use Tests\TestCase;

/**
 * DEF-24: el favicon (ICO y SVG) y el icono de iOS eran los del kit de inicio de Laravel. Ahora muestran la
 * marca de la plataforma (`app-logo-icon.tsx`). El color se comprueba en el navegador (`e2e-26`).
 */
class BrandIconsTest extends TestCase
{
    private const LARAVEL_FAVICON_ICO_SHA256 = '4606a56e6ef3f5ec39201497f57069d5457ce9cea25227134d0ba378788e9070';

    private const LARAVEL_APPLE_TOUCH_ICON_SHA256 = '4001aa032ff113e1a268a9bbf1ab0fd9949439f9f54a85895956eb323aba977d';

    public function test_svg_favicon_draws_the_platform_mark_and_adapts_to_dark_browsers(): void
    {
        $svg = (string) file_get_contents(public_path('favicon.svg'));

        $this->assertStringNotContainsStringIgnoringCase('#FF2D20', $svg);
        $this->assertStringContainsString('<title>SaaS Reclutamiento</title>', $svg);
        $this->assertStringContainsString('prefers-color-scheme: dark', $svg);
    }

    public function test_ico_favicon_is_not_the_laravel_icon_and_carries_the_small_sizes(): void
    {
        $ico = (string) file_get_contents(public_path('favicon.ico'));

        $this->assertNotSame(self::LARAVEL_FAVICON_ICO_SHA256, hash('sha256', $ico));

        $header = unpack('vreserved/vtype/vcount', substr($ico, 0, 6));
        $this->assertSame(1, $header['type'], 'Cabecera ICO');

        $sizes = [];
        for ($i = 0; $i < $header['count']; $i++) {
            $entry = unpack('Cwidth/Cheight', substr($ico, 6 + 16 * $i, 2));
            $sizes[] = $entry['width'] === 0 ? 256 : $entry['width'];
        }
        sort($sizes);

        $this->assertSame([16, 32, 48], $sizes);
    }

    public function test_apple_touch_icon_is_an_opaque_180_pixel_png(): void
    {
        $png = (string) file_get_contents(public_path('apple-touch-icon.png'));

        $this->assertNotSame(self::LARAVEL_APPLE_TOUCH_ICON_SHA256, hash('sha256', $png));
        $this->assertSame([180, 180, IMAGETYPE_PNG], array_slice(getimagesizefromstring($png) ?: [], 0, 3));
        // Tipo de color del IHDR: 2 es RGB sin alfa. iOS pinta de negro lo transparente.
        $this->assertSame(2, ord($png[25]));
    }

    public function test_root_view_still_links_the_three_icons(): void
    {
        $this->get(route('login'))
            ->assertOk()
            ->assertSee('<link rel="icon" href="/favicon.ico" sizes="any">', false)
            ->assertSee('<link rel="icon" href="/favicon.svg" type="image/svg+xml">', false)
            ->assertSee('<link rel="apple-touch-icon" href="/apple-touch-icon.png">', false);
    }
}
