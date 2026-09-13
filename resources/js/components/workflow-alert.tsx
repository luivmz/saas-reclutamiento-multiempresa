import { usePage } from '@inertiajs/react';
import { AlertTriangle } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

export function WorkflowAlert() {
    const { errors } = usePage().props;
    const message = (errors as Record<string, string> | undefined)?.workflow;

    if (!message) {
        return null;
    }

    return (
        <Alert variant="destructive" data-cy="workflow-error">
            <AlertTriangle />
            <AlertTitle>No se pudo completar la operación</AlertTitle>
            <AlertDescription>{message}</AlertDescription>
        </Alert>
    );
}
