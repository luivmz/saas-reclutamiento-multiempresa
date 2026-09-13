<?php

namespace Tests\Unit\Enums;

use App\Enums\ApplicationStatus;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;

class ApplicationStatusTest extends TestCase
{
    /**
     * @return array<string, array{ApplicationStatus, ApplicationStatus, bool}>
     */
    public static function transitions(): array
    {
        return [
            'postulado → preseleccionado' => [ApplicationStatus::Submitted, ApplicationStatus::Shortlisted, true],
            'postulado → descartado' => [ApplicationStatus::Submitted, ApplicationStatus::Discarded, true],
            'postulado → finalista' => [ApplicationStatus::Submitted, ApplicationStatus::Finalist, false],
            'preseleccionado → en_evaluacion' => [ApplicationStatus::Shortlisted, ApplicationStatus::Evaluation, true],
            'preseleccionado → en_entrevista' => [ApplicationStatus::Shortlisted, ApplicationStatus::Interview, true],
            'en_evaluacion → en_entrevista' => [ApplicationStatus::Evaluation, ApplicationStatus::Interview, true],
            'en_evaluacion → finalista' => [ApplicationStatus::Evaluation, ApplicationStatus::Finalist, true],
            'en_entrevista → finalista' => [ApplicationStatus::Interview, ApplicationStatus::Finalist, true],
            'finalista → seleccionado' => [ApplicationStatus::Finalist, ApplicationStatus::Selected, true],
            'finalista → no_seleccionado' => [ApplicationStatus::Finalist, ApplicationStatus::NotSelected, true],
            'seleccionado → descartado' => [ApplicationStatus::Selected, ApplicationStatus::Discarded, false],
            'descartado → preseleccionado' => [ApplicationStatus::Discarded, ApplicationStatus::Shortlisted, false],
            'no_seleccionado → finalista' => [ApplicationStatus::NotSelected, ApplicationStatus::Finalist, false],
        ];
    }

    #[DataProvider('transitions')]
    public function test_transition_rules(ApplicationStatus $from, ApplicationStatus $to, bool $allowed): void
    {
        $this->assertSame($allowed, $from->canTransitionTo($to));
    }

    public function test_selection_outcomes_are_not_manual_targets(): void
    {
        $this->assertSame([
            ApplicationStatus::Shortlisted,
            ApplicationStatus::Evaluation,
            ApplicationStatus::Interview,
            ApplicationStatus::Finalist,
            ApplicationStatus::Discarded,
        ], ApplicationStatus::manualTargets());
    }

    public function test_terminal_statuses(): void
    {
        $terminal = array_values(array_filter(ApplicationStatus::cases(), fn (ApplicationStatus $s) => $s->isTerminal()));

        $this->assertSame([ApplicationStatus::Selected, ApplicationStatus::NotSelected, ApplicationStatus::Discarded], $terminal);
    }
}
