<?php

namespace App\Services\Ranking;

use App\Exceptions\BusinessRuleException;

class InvalidRankingInput extends BusinessRuleException
{
    public static function because(string $reason): self
    {
        return new self('No es posible calcular el ranking: '.$reason);
    }
}
