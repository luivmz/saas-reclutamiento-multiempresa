<?php

namespace App\Models;

use App\Enums\EvidenceSource;
use App\Enums\EvidenceType;
use App\Models\Concerns\BelongsToOrganization;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\HasOne;
use Illuminate\Support\Carbon;

/**
 * EXPERIMENTAL (F37 flow, exp/evidencias-ml02). One immutable version of a fictitious evidence record declared by
 * a person about an application. A correction is a new row that supersedes this one (R-04); the database refuses
 * UPDATE and DELETE. The system never reads the description to decide anything about the person.
 *
 * @property int $id
 * @property int $organization_id
 * @property int $application_id
 * @property int|null $supersedes_id
 * @property EvidenceType $type
 * @property EvidenceSource $source
 * @property string $description
 * @property int|null $registered_by
 * @property Carbon $created_at
 * @property-read Application $application
 * @property-read User|null $author
 * @property-read EvidenceItem|null $supersedes
 * @property-read EvidenceItem|null $supersededBy
 */
class EvidenceItem extends Model
{
    use BelongsToOrganization;

    public const UPDATED_AT = null;

    protected function casts(): array
    {
        return [
            'type' => EvidenceType::class,
            'source' => EvidenceSource::class,
            'created_at' => 'datetime',
        ];
    }

    public function code(): string
    {
        return 'EVD-'.str_pad((string) $this->id, 5, '0', STR_PAD_LEFT);
    }

    /**
     * @return BelongsTo<Application, $this>
     */
    public function application(): BelongsTo
    {
        return $this->belongsTo(Application::class);
    }

    /**
     * @return BelongsTo<User, $this>
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class, 'registered_by');
    }

    /**
     * @return BelongsTo<EvidenceItem, $this>
     */
    public function supersedes(): BelongsTo
    {
        return $this->belongsTo(self::class, 'supersedes_id');
    }

    /**
     * @return HasOne<EvidenceItem, $this>
     */
    public function supersededBy(): HasOne
    {
        return $this->hasOne(self::class, 'supersedes_id');
    }

    /**
     * @return HasMany<EvidenceEvent, $this>
     */
    public function events(): HasMany
    {
        return $this->hasMany(EvidenceEvent::class);
    }
}
