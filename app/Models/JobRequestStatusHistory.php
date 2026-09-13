<?php

namespace App\Models;

use App\Enums\JobRequestStatus;
use App\Models\Concerns\BelongsToOrganization;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Support\Carbon;

/**
 * @property int $id
 * @property int $organization_id
 * @property int $job_request_id
 * @property JobRequestStatus|null $from_status
 * @property JobRequestStatus $to_status
 * @property int $changed_by
 * @property string|null $comment
 * @property Carbon $created_at
 * @property-read User $author
 */
class JobRequestStatusHistory extends Model
{
    use BelongsToOrganization;

    public const UPDATED_AT = null;

    protected $guarded = ['id'];

    protected function casts(): array
    {
        return [
            'from_status' => JobRequestStatus::class,
            'to_status' => JobRequestStatus::class,
            'created_at' => 'datetime',
        ];
    }

    /**
     * @return BelongsTo<JobRequest, $this>
     */
    public function jobRequest(): BelongsTo
    {
        return $this->belongsTo(JobRequest::class);
    }

    /**
     * @return BelongsTo<User, $this>
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class, 'changed_by');
    }
}
