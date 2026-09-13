<?php

namespace App\Exceptions;

class InvalidStateTransition extends BusinessRuleException
{
    public static function between(string $entity, string $from, string $to): self
    {
        return new self("No es posible cambiar {$entity} de «{$from}» a «{$to}».");
    }
}
