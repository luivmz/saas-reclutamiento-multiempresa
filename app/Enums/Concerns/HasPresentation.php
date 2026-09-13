<?php

namespace App\Enums\Concerns;

trait HasPresentation
{
    abstract public function label(): string;

    abstract public function tone(): string;

    /**
     * @return array{value: string, label: string, tone: string}
     */
    public function present(): array
    {
        return [
            'value' => $this->value,
            'label' => $this->label(),
            'tone' => $this->tone(),
        ];
    }

    /**
     * @return list<array{value: string, label: string, tone: string}>
     */
    public static function options(): array
    {
        return array_map(fn (self $case) => $case->present(), self::cases());
    }

    /**
     * @return list<string>
     */
    public static function values(): array
    {
        return array_column(self::cases(), 'value');
    }
}
