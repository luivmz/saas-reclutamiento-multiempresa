import { Form, Head, Link } from '@inertiajs/react';
import JobRequestController from '@/actions/App/Http/Controllers/JobRequests/JobRequestController';
import { JobRequestFields } from '@/components/job-requests/job-request-fields';
import { PageContainer, PageHeader, Section } from '@/components/page';
import { Button } from '@/components/ui/button';
import { Spinner } from '@/components/ui/spinner';
import type { Presented } from '@/types';

export default function CreateJobRequest({
    contractTypes,
}: {
    contractTypes: Presented[];
}) {
    return (
        <>
            <Head title="Nuevo requerimiento" />
            <PageContainer className="max-w-3xl">
                <PageHeader
                    title="Nuevo requerimiento de personal"
                    description="Se registra como borrador. Después podrá revisarlo y enviarlo a RR. HH. (RF-01)."
                />
                <Form
                    {...JobRequestController.store.form()}
                    disableWhileProcessing
                >
                    {({ errors, processing }) => (
                        <Section>
                            <JobRequestFields
                                contractTypes={contractTypes}
                                errors={errors}
                            />
                            <div className="mt-6 flex flex-wrap justify-end gap-2 border-t pt-5">
                                <Button variant="outline" asChild>
                                    <Link href={JobRequestController.index()}>
                                        Cancelar
                                    </Link>
                                </Button>
                                <Button
                                    type="submit"
                                    disabled={processing}
                                    data-cy="save-job-request"
                                >
                                    {processing && <Spinner />}
                                    Registrar requerimiento
                                </Button>
                            </div>
                        </Section>
                    )}
                </Form>
            </PageContainer>
        </>
    );
}

CreateJobRequest.layout = {
    breadcrumbs: [
        { title: 'Requerimientos', href: JobRequestController.index() },
        { title: 'Nuevo', href: JobRequestController.create() },
    ],
};
