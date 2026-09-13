<?php

namespace App\Http\Controllers\Documents;

use App\Http\Controllers\Controller;
use App\Models\CandidateDocument;
use Illuminate\Support\Facades\Gate;
use Illuminate\Support\Facades\Storage;
use Symfony\Component\HttpFoundation\StreamedResponse;

class CandidateDocumentDownloadController extends Controller
{
    public function __invoke(CandidateDocument $document): StreamedResponse
    {
        Gate::authorize('download', $document);

        $disk = Storage::disk('local');
        abort_unless($disk->exists($document->stored_path), 404);

        return $disk->download($document->stored_path, $document->original_name, [
            'Content-Type' => $document->mime_type,
            'X-Content-Type-Options' => 'nosniff',
        ]);
    }
}
