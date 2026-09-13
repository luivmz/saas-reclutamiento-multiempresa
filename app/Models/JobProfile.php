<?php

namespace App\Models;

use App\Models\Concerns\BelongsToOrganization;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/**
 * @property int $id
 * @property int $organization_id
 * @property int $vacancy_id
 * @property string $education
 * @property string $experience
 * @property string $functions
 * @property string $competencies
 */
#[Fillable(['education', 'experience', 'functions', 'competencies'])]
class JobProfile extends Model
{
    use BelongsToOrganization;

    /**
     * @return BelongsTo<Vacancy, $this>
     */
    public function vacancy(): BelongsTo
    {
        return $this->belongsTo(Vacancy::class);
    }
}
