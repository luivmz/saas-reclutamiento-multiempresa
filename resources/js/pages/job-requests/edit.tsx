import { Form, Head, Link } from '@inertiajs/react';
import { AlertTriangle } from 'lucide-react';
import JobRequestController from '@/actions/App/Http/Controllers/JobRequests/JobRequestController';
import { JobRequestFields } from '@/components/job-requests/job-request-fields';
import { PageContainer, PageHeader, Section } from '@/components/page';
import { WorkflowAlert } from '@/components/workflow-alert';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
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
                    eyebrow={
                        <span className="font-mono text-xs">
                            {jobRequest.code}
                        </span>
                    }
                    title="Corregir requerimiento"
                    description="Actualice la información observada y vuelva a enviarla a RR. HH. (RF-02)."
                />
                <WorkflowAlert />
                {jobRequest.observation && (
                    <Alert data-cy="observation-alert">
                        <AlertTriangle />
                        <AlertTitle>Observación de RR. HH.</AlertTitle>
                        <AlertDescription>
                            {jobRequest.observation}
                        </AlertDescription>
                    </Alert>
                )}
                <Form
                    {...JobRequestController.update.form(jobRequest.id)}
                    disableWhileProcessing
                >
                    {({ errors, processing }) => (
                        <Section>
                            <JobRequestFields
                                contractTypes={contractTypes}
                                defaults={jobRequest}
                                errors={errors}
                            />
                            <div className="mt-6 flex flex-wrap justify-end gap-2 border-t pt-5">
                                <Button variant="outline" asChild>
                                    <Link
                                        href={JobRequestController.show(
                                            jobRequest.id,
                                        )}
                                    >
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
                            </div>
                        </Section>
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
