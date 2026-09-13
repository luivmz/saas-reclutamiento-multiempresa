import { Form, Head } from '@inertiajs/react';
import { AlertTriangle, CheckCircle2, FileText, Upload } from 'lucide-react';
import CandidateCvController from '@/actions/App/Http/Controllers/Candidates/CandidateCvController';
import CandidateProfileController from '@/actions/App/Http/Controllers/Candidates/CandidateProfileController';
import { FormField, NativeSelect } from '@/components/form-controls';
import InputError from '@/components/input-error';
import { PageContainer, PageHeader } from '@/components/page';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Spinner } from '@/components/ui/spinner';
import { Textarea } from '@/components/ui/textarea';
import { formatDateTime, formatFileSize } from '@/lib/format';
import type { DocumentSummary, Presented } from '@/types';

type ProfileForm = {
    phone: string | null;
    city: string | null;
    education_level: string | null;
    professional_title: string | null;
    years_of_experience: number | null;
    summary: string | null;
};

type Props = {
    profile: ProfileForm | null;
    cv: DocumentSummary | null;
    missingFields: string[];
    educationLevels: Presented[];
    cvMaxKb: number;
};

export default function CandidateProfilePage({
    profile,
    cv,
    missingFields,
    educationLevels,
    cvMaxKb,
}: Props) {
    const pending = [...missingFields, ...(cv ? [] : ['CV en PDF'])];

    return (
        <>
            <Head title="Mi perfil" />
            <PageContainer className="max-w-5xl">
                <PageHeader
                    title="Mi perfil de postulante"
                    description="RF-09 · Mantenga actualizada su información y su CV para postular a las convocatorias."
                />

                {pending.length > 0 ? (
                    <Alert data-cy="profile-incomplete">
                        <AlertTriangle />
                        <AlertTitle>Perfil incompleto</AlertTitle>
                        <AlertDescription>
                            Para postular complete: {pending.join(', ')}.
                        </AlertDescription>
                    </Alert>
                ) : (
                    <Alert data-cy="profile-complete">
                        <CheckCircle2 className="text-emerald-600" />
                        <AlertTitle>Perfil listo para postular</AlertTitle>
                        <AlertDescription>
                            Su información y su CV están completos.
                        </AlertDescription>
                    </Alert>
                )}

                <div className="grid gap-6 lg:grid-cols-3">
                    <Card className="lg:col-span-2">
                        <CardHeader>
                            <CardTitle>Datos profesionales</CardTitle>
                            <CardDescription>
                                Solo solicitamos la información necesaria para el proceso.
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <Form
                                {...CandidateProfileController.update.form()}
                                options={{ preserveScroll: true }}
                                className="grid gap-5 md:grid-cols-2"
                            >
                                {({ errors, processing }) => (
                                    <>
                                        <FormField label="Teléfono" htmlFor="phone" error={errors.phone}>
                                            <Input id="phone" name="phone" defaultValue={profile?.phone ?? ''} placeholder="9XXXXXXXX" data-cy="profile-phone" />
                                        </FormField>
                                        <FormField label="Ciudad" htmlFor="city" error={errors.city}>
                                            <Input id="city" name="city" defaultValue={profile?.city ?? ''} data-cy="profile-city" />
                                        </FormField>
                                        <FormField label="Nivel educativo" htmlFor="education_level" error={errors.education_level}>
                                            <NativeSelect
                                                id="education_level"
                                                name="education_level"
                                                options={educationLevels}
                                                placeholder="Seleccione…"
                                                defaultValue={profile?.education_level ?? ''}
                                                data-cy="profile-education-level"
                                            />
                                        </FormField>
                                        <FormField label="Años de experiencia" htmlFor="years_of_experience" error={errors.years_of_experience}>
                                            <Input
                                                id="years_of_experience"
                                                name="years_of_experience"
                                                type="number"
                                                min={0}
                                                max={60}
                                                defaultValue={profile?.years_of_experience ?? ''}
                                                data-cy="profile-years"
                                            />
                                        </FormField>
                                        <FormField label="Título u ocupación" htmlFor="professional_title" error={errors.professional_title} className="md:col-span-2">
                                            <Input id="professional_title" name="professional_title" defaultValue={profile?.professional_title ?? ''} data-cy="profile-title" />
                                        </FormField>
                                        <FormField label="Resumen profesional" htmlFor="summary" error={errors.summary} hint="Opcional." className="md:col-span-2">
                                            <Textarea id="summary" name="summary" rows={4} defaultValue={profile?.summary ?? ''} data-cy="profile-summary" />
                                        </FormField>
                                        <div className="flex justify-end md:col-span-2">
                                            <Button type="submit" disabled={processing} data-cy="save-profile">
                                                {processing && <Spinner />}
                                                Guardar perfil
                                            </Button>
                                        </div>
                                    </>
                                )}
                            </Form>
                        </CardContent>
                    </Card>

                    <Card className="h-fit">
                        <CardHeader>
                            <CardTitle>Currículum vitae</CardTitle>
                            <CardDescription>
                                PDF de hasta {Math.round(cvMaxKb / 1024)} MB. Se almacena de forma privada.
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            {cv ? (
                                <a href={cv.download_url} className="hover:bg-accent flex items-center gap-3 rounded-lg border p-3 text-sm" data-cy="current-cv">
                                    <FileText className="text-muted-foreground size-5 shrink-0" />
                                    <span className="min-w-0">
                                        <span className="block truncate font-medium">{cv.original_name}</span>
                                        <span className="text-muted-foreground text-xs">
                                            {formatFileSize(cv.size_bytes)} · {formatDateTime(cv.uploaded_at)}
                                        </span>
                                    </span>
                                </a>
                            ) : (
                                <p className="text-muted-foreground text-sm" data-cy="no-cv">
                                    Aún no ha cargado su CV.
                                </p>
                            )}
                            <Form
                                {...CandidateCvController.form()}
                                resetOnSuccess
                                options={{ preserveScroll: true }}
                                className="space-y-3"
                            >
                                {({ errors, processing }) => (
                                    <>
                                        <Input type="file" name="cv" accept="application/pdf,.pdf" aria-label="Archivo PDF del CV" data-cy="cv-input" />
                                        <InputError message={errors.cv} />
                                        <Button type="submit" variant="outline" disabled={processing} className="w-full" data-cy="upload-cv">
                                            {processing ? <Spinner /> : <Upload />}
                                            {cv ? 'Reemplazar CV' : 'Cargar CV'}
                                        </Button>
                                    </>
                                )}
                            </Form>
                        </CardContent>
                    </Card>
                </div>
            </PageContainer>
        </>
    );
}

CandidateProfilePage.layout = {
    breadcrumbs: [{ title: 'Mi perfil', href: CandidateProfileController.edit() }],
};
