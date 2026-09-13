import { Form, Head, Link } from '@inertiajs/react';
import { AlertTriangle } from 'lucide-react';
import JobRequestController from '@/actions/App/Http/Controllers/JobRequests/JobRequestController';
import { JobRequestFields } from '@/components/job-requests/job-request-fields';
import { PageContainer, PageHeader } from '@/components/page';
import { WorkflowAlert } from '@/components/workflow-alert';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Spinner } from '@/components/ui/spinner';
import type { JobRequest, Presented } from '@/types';

export default function EditJobRequest({
    jobRequest,
    contractTypes,
}: {
    jobRequest: JobRequest;
    contractTypes: Presented[];
}) {
    return (
        <>
            <Head title={`Corregir ${jobRequest.code}`} />
            <PageContainer className="max-w-3xl">
                <PageHeader
                    eyebrow={jobRequest.code}
                    title="Corregir requerimiento"
                    description="RF-02 · Actualice la información y vuelva a enviarla a RR. HH."
                />
                <WorkflowAlert />
                {jobRequest.observation && (
                    <Alert data-cy="observation-alert">
                        <AlertTriangle />
                        <AlertTitle>Observación de RR. HH.</AlertTitle>
                        <AlertDescription>{jobRequest.observation}</AlertDescription>
                    </Alert>
                )}
                <Form
                    {...JobRequestController.update.form(jobRequest.id)}
                    disableWhileProcessing
                >
                    {({ errors, processing }) => (
                        <Card>
                            <CardContent>
                                <JobRequestFields
                                    contractTypes={contractTypes}
                                    defaults={jobRequest}
                                    errors={errors}
                                />
                            </CardContent>
                            <CardFooter className="justify-end gap-2 border-t pt-6">
                                <Button variant="outline" asChild>
                                    <Link href={JobRequestController.show(jobRequest.id)}>
                                        Cancelar
                                    </Link>
                                </Button>
                                <Button
                                    type="submit"
                                    disabled={processing}
                                    data-cy="save-job-request"
                                >
                                    {processing && <Spinner />}
                                    Guardar corrección
                                </Button>
                            </CardFooter>
                        </Card>
                    )}
                </Form>
            </PageContainer>
        </>
    );
}

EditJobRequest.layout = {
    breadcrumbs: [
        { title: 'Requerimientos', href: JobRequestController.index() },
        { title: 'Corregir', href: JobRequestController.index() },
    ],
};
