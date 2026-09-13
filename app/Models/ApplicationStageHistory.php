<?php

namespace App\Models;

use App\Enums\ApplicationStatus;
use App\Models\Concerns\BelongsToOrganization;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Support\Carbon;

/**
 * @property int $id
 * @property int $organization_id
 * @property int $application_id
 * @property ApplicationStatus|null $from_status
 * @property ApplicationStatus $to_status
 * @property int $changed_by
 * @property string|null $comment
 * @property Carbon $created_at
 * @property-read User $author
 */
class ApplicationStageHistory extends Model
{
    use BelongsToOrganization;

    public const UPDATED_AT = null;

    protected function casts(): array
    {
        return [
            'from_status' => ApplicationStatus::class,
            'to_status' => ApplicationStatus::class,
            'created_at' => 'datetime',
        ];
    }

    /**
     * @return array<string, mixed>
     */
    public function toTimelineEntry(): array
    {
        return [
            'id' => $this->id,
            'from' => $this->from_status?->present(),
            'to' => $this->to_status->present(),
            'author' => $this->author->name,
            'comment' => $this->comment,
            'created_at' => $this->created_at->toIso8601String(),
        ];
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
        return $this->belongsTo(User::class, 'changed_by');
    }
}
