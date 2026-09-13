<?php

namespace App\Exceptions;

use App\Http\Support\Toast;
use DomainException;
use Illuminate\Contracts\Debug\ShouldntReport;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

/**
 * A business rule prevented the operation. Expected behaviour, so it is not reported as an application error.
 */
class BusinessRuleException extends DomainException implements ShouldntReport
{
    public function __construct(string $message, private readonly string $errorKey = 'workflow')
    {
        parent::__construct($message);
    }

    public function errorKey(): string
    {
        return $this->errorKey;
    }

    public function render(Request $request): JsonResponse|RedirectResponse
    {
        if ($request->expectsJson() && ! $request->header('X-Inertia')) {
            return response()->json([
                'message' => $this->getMessage(),
                'errors' => [$this->errorKey => [$this->getMessage()]],
            ], 422);
        }

        Toast::error($this->getMessage());

        return back()->withErrors([$this->errorKey => $this->getMessage()]);
    }
}
