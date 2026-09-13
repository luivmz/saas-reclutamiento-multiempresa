<?php

namespace App\Models;

use App\Enums\DocumentType;
use App\Enums\EducationLevel;
use Database\Factories\CandidateProfileFactory;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\HasOne;

/**
 * @property int $id
 * @property int $user_id
 * @property string|null $phone
 * @property string|null $city
 * @property EducationLevel|null $education_level
 * @property string|null $professional_title
 * @property int|null $years_of_experience
 * @property string|null $summary
 * @property-read User $user
 * @property-read CandidateDocument|null $latestCv
 */
#[Fillable(['phone', 'city', 'education_level', 'professional_title', 'years_of_experience', 'summary'])]
class CandidateProfile extends Model
{
    /** @use HasFactory<CandidateProfileFactory> */
    use HasFactory;

    /**
     * Fields required before applying (see docs/assumptions.md A-11).
     */
    public const REQUIRED_FIELDS = [
        'phone' => 'teléfono',
        'city' => 'ciudad',
        'education_level' => 'nivel educativo',
        'professional_title' => 'título u ocupación',
        'years_of_experience' => 'años de experiencia',
    ];

    protected function casts(): array
    {
        return [
            'education_level' => EducationLevel::class,
            'years_of_experience' => 'integer',
        ];
    }

    /**
     * @return list<string>
     */
    public function missingFields(): array
    {
        $missing = [];

        foreach (self::REQUIRED_FIELDS as $field => $label) {
            $value = $this->getAttribute($field);

            if ($value === null || $value === '') {
                $missing[] = $label;
            }
        }

        return $missing;
    }

    public function isComplete(): bool
    {
        return $this->missingFields() === [];
    }

    /**
     * @return BelongsTo<User, $this>
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * @return HasMany<CandidateDocument, $this>
     */
    public function documents(): HasMany
    {
        return $this->hasMany(CandidateDocument::class);
    }

    /**
     * @return HasOne<CandidateDocument, $this>
     */
    public function latestCv(): HasOne
    {
        return $this->hasOne(CandidateDocument::class)
            ->ofMany(['id' => 'max'], fn (Builder $query) => $query->where('type', DocumentType::Cv));
    }
}
