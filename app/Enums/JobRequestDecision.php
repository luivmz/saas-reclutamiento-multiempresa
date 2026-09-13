<?php

namespace App\Enums;

enum JobRequestDecision: string
{
    case Approve = 'aprobar';
    case Reject = 'rechazar';
}
