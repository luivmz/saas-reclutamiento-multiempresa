<?php

namespace Tests\Unit\Enums;

use App\Enums\JobRequestStatus;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;

class JobRequestStatusTest extends TestCase
{
    /**
     * @return array<string, array{JobRequestStatus, JobRequestStatus, bool}>
     */
    public static function transitions(): array
    {
        return [
            'borrador → enviado' => [JobRequestStatus::Draft, JobRequestStatus::Submitted, true],
            'enviado → observado' => [JobRequestStatus::Submitted, JobRequestStatus::Observed, true],
            'enviado → validado' => [JobRequestStatus::Submitted, JobRequestStatus::Validated, true],
            'observado → enviado' => [JobRequestStatus::Observed, JobRequestStatus::Submitted, true],
            'validado → aprobado' => [JobRequestStatus::Validated, JobRequestStatus::Approved, true],
            'validado → rechazado' => [JobRequestStatus::Validated, JobRequestStatus::Rejected, true],
            'borrador → aprobado' => [JobRequestStatus::Draft, JobRequestStatus::Approved, false],
            'enviado → aprobado' => [JobRequestStatus::Submitted, JobRequestStatus::Approved, false],
            'observado → validado' => [JobRequestStatus::Observed, JobRequestStatus::Validated, false],
            'aprobado → rechazado' => [JobRequestStatus::Approved, JobRequestStatus::Rejected, false],
            'rechazado → enviado' => [JobRequestStatus::Rejected, JobRequestStatus::Submitted, false],
        ];
    }

    #[DataProvider('transitions')]
    public function test_transition_rules(JobRequestStatus $from, JobRequestStatus $to, bool $allowed): void
    {
        $this->assertSame($allowed, $from->canTransitionTo($to));
    }

    public function test_only_draft_and_observed_requests_are_editable(): void
    {
        $editable = array_values(array_filter(JobRequestStatus::cases(), fn (JobRequestStatus $s) => $s->isEditable()));

        $this->assertSame([JobRequestStatus::Draft, JobRequestStatus::Observed], $editable);
    }

    public function test_approved_and_rejected_are_terminal(): void
    {
        $this->assertSame([], JobRequestStatus::Approved->allowedTransitions());
        $this->assertSame([], JobRequestStatus::Rejected->allowedTransitions());
    }
}
