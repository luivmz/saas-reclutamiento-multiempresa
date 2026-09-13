<?php

$requiredTotal = env('RECRUITMENT_WEIGHTS_TOTAL', 100);

return [

    /*
    | RF-20: if set, the weights of a vacancy's criteria must add up to this value.
    | Set RECRUITMENT_WEIGHTS_TOTAL=null to only require positive weights (see docs/assumptions.md).
    */
    'weights' => [
        'required_total' => $requiredTotal === null || $requiredTotal === '' ? null : (float) $requiredTotal,
    ],

    'cv' => [
        'max_kb' => (int) env('CV_MAX_KB', 5120),
        'mimes' => ['pdf'],
    ],

];
