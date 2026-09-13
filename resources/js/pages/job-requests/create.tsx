import { Form, Head, Link } from '@inertiajs/react';
import JobRequestController from '@/actions/App/Http/Controllers/JobRequests/JobRequestController';
import { JobRequestFields } from '@/components/job-requests/job-request-fields';
import { PageContainer, PageHeader } from '@/components/page';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
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
                    description="RF-01 · Se registra como borrador. Después podrá revisarlo y enviarlo a RR. HH."
                />
                <Form {...JobRequestController.store.form()} disableWhileProcessing>
                    {({ errors, processing }) => (
                        <Card>
                            <CardContent>
                                <JobRequestFields
                                    contractTypes={contractTypes}
                                    errors={errors}
                                />
                            </CardContent>
                            <CardFooter className="justify-end gap-2 border-t pt-6">
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
                            </CardFooter>
                        </Card>
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
