<?php

namespace App\Services\Audit;

use App\Enums\AuditAction;
use App\Models\AuditLog;
use App\Models\User;
use Illuminate\Contracts\Auth\Factory as AuthFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Http\Request;

class AuditLogger
{
    private const SENSITIVE_KEY_PATTERN = '/password|token|secret|remember|cookie|authorization|api[_-]?key|cv_content|file_contents/i';

    public function __construct(
        private readonly AuthFactory $auth,
        private readonly Request $request,
    ) {}

    /**
     * @param  array<string, mixed>  $metadata
     */
    public function record(AuditAction $action, Model $subject, array $metadata = [], ?User $actor = null): AuditLog
    {
        $actor ??= $this->currentUser();

        $log = new AuditLog;
        $log->forceFill([
            'organization_id' => $this->resolveOrganizationId($subject, $actor),
            'user_id' => $actor?->getKey(),
            'action' => $action,
            'auditable_type' => $subject->getMorphClass(),
            'auditable_id' => $subject->getKey(),
            'metadata' => $this->sanitize($metadata),
            'ip_address' => $this->request->ip(),
        ])->save();

        return $log;
    }

    private function currentUser(): ?User
    {
        $user = $this->auth->guard()->user();

        return $user instanceof User ? $user : null;
    }

    private function resolveOrganizationId(Model $subject, ?User $actor): ?int
    {
        if (array_key_exists('organization_id', $subject->getAttributes())) {
            return $subject->getAttribute('organization_id');
        }

        return $actor?->organization_id;
    }

    /**
     * @param  array<string, mixed>  $metadata
     * @return array<string, mixed>
     */
    private function sanitize(array $metadata): array
    {
        $clean = [];

        foreach ($metadata as $key => $value) {
            if (is_string($key) && preg_match(self::SENSITIVE_KEY_PATTERN, $key)) {
                continue;
            }

            $clean[$key] = is_array($value) ? $this->sanitize($value) : $value;
        }

        return $clean;
    }
}
