<?php

namespace Tests\Feature\Routing;

use App\Models\Vacancy;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Inertia\Inertia;
use Inertia\Testing\AssertableInertia as Assert;
use Tests\TestCase;

class TrustedProxiesTest extends TestCase
{
    use RefreshDatabase;

    public function test_trusted_proxy_generates_https_pagination_and_assets(): void
    {
        $this->configureProxyList(' 192.0.2.10, 2001:db8:20::/64 ');

        $this->assertListingUrls('192.0.2.10', 'https', 'https://jobs.example.test');
    }

    public function test_untrusted_origin_cannot_change_the_scheme(): void
    {
        $this->configureProxyList('192.0.2.10');

        $this->assertListingUrls('192.0.2.11', 'https', 'http://jobs.example.test');
    }

    public function test_localhost_uses_http_without_trusted_proxies(): void
    {
        $this->configureProxyList('');

        $url = 'http://localhost:8000';
        $this->assertListingUrls('127.0.0.1', null, $url, $url);
    }

    public function test_wildcards_and_invalid_ranges_do_not_enable_proxy_trust(): void
    {
        $this->configureProxyList('*, **, REMOTE_ADDR, 0.0.0.0/0, ::/0, 192.0.2.10/33, 2001:db8::/129');

        $this->assertSame([], config('trustedproxy.proxies'));
        $this->assertListingUrls('192.0.2.11', 'https', 'http://jobs.example.test');
    }

    private function configureProxyList(string $value): void
    {
        // Load the real config with a fixture after Dotenv has read the runner's .env.
        $previous = $_SERVER['TRUSTED_PROXIES'] ?? null;
        $_SERVER['TRUSTED_PROXIES'] = $value;

        try {
            config(['trustedproxy' => require config_path('trustedproxy.php')]);
        } finally {
            if ($previous === null) {
                unset($_SERVER['TRUSTED_PROXIES']);
            } else {
                $_SERVER['TRUSTED_PROXIES'] = $previous;
            }
        }
    }

    private function assertListingUrls(
        string $peer,
        ?string $forwardedProto,
        string $expectedBase,
        string $requestBase = 'http://jobs.example.test',
    ): void {
        Vacancy::factory()->count(13)->published()->create(['title' => 'Docente']);
        Inertia::share('testAssetUrl', fn (): string => asset('favicon.svg'));

        $server = ['REMOTE_ADDR' => $peer];
        if ($forwardedProto !== null) {
            $server['HTTP_X_FORWARDED_PROTO'] = $forwardedProto;
            $server['HTTP_X_FORWARDED_HOST'] = 'ignored.example.test';
            $server['HTTP_X_FORWARDED_PORT'] = '8443';
        }

        $this->withServerVariables($server)
            ->get($requestBase.'/empleos?q=docente')
            ->assertOk()
            ->assertInertia(fn (Assert $page) => $page
                ->component('jobs/index')
                ->where('vacancies.meta.path', $expectedBase.'/empleos')
                ->where('vacancies.links.next', $expectedBase.'/empleos?q=docente&page=2')
                ->where('testAssetUrl', $expectedBase.'/favicon.svg')
            );
    }
}
