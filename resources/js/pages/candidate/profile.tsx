import { Form, Head, Link } from '@inertiajs/react';
import {
    AlertTriangle,
    ArrowLeft,
    CheckCircle2,
    FileText,
    Upload,
} from 'lucide-react';
import CandidateCvController from '@/actions/App/Http/Controllers/Candidates/CandidateCvController';
import CandidateProfileController from '@/actions/App/Http/Controllers/Candidates/CandidateProfileController';
import { FormField, NativeSelect } from '@/components/form-controls';
import InputError from '@/components/input-error';
import { PageContainer, PageHeader, Section } from '@/components/page';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Spinner } from '@/components/ui/spinner';
import { Textarea } from '@/components/ui/textarea';
import { formatDate, formatDateTime, formatFileSize } from '@/lib/format';
import { index as jobsIndex, show as jobsShow } from '@/routes/jobs';
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
    retorno: Retorno | null;
};

/** Convocatoria de la que llegó el postulante (ConvocatoriaDeRetorno). */
type Retorno =
    | { disponible: false }
    | {
          disponible: true;
          id: number;
          title: string;
          accepts_applications: boolean;
          application_deadline_passed: boolean;
          closes_at: string | null;
      };

/**
 * Camino de vuelta a la convocatoria. Volver solo abre su detalle: ahí la
 * persona decide si postula. Si la convocatoria cerró o venció, se dice.
 */
function ReturnToVacancy({
    retorno,
    ready,
}: {
    retorno: Retorno;
    ready: boolean;
}) {
    if (!retorno.disponible) {
        return (
            <Alert data-cy="profile-return-unavailable">
                <AlertTriangle />
                <AlertTitle>
                    La convocatoria que estaba viendo ya no está disponible
                </AlertTitle>
                <AlertDescription>
                    <p>
                        Dejó de publicarse. Puede revisar las convocatorias
                        vigentes.
                    </p>
                    <Link
                        href={jobsIndex()}
                        className="text-primary font-medium underline underline-offset-4"
                    >
                        Ver convocatorias
                    </Link>
                </AlertDescription>
            </Alert>
        );
    }

    if (!retorno.accepts_applications) {
        return (
            <Alert data-cy="profile-return-closed">
                <AlertTriangle />
                <AlertTitle className="[overflow-wrap:anywhere]">
                    {retorno.title}
                </AlertTitle>
                <AlertDescription>
                    <p>
                        {retorno.application_deadline_passed
                            ? `El plazo de postulación venció el ${formatDate(retorno.closes_at)}.`
                            : 'La convocatoria no está recibiendo postulaciones.'}
                    </p>
                    <p className="flex flex-wrap gap-x-4 gap-y-1">
                        <Link
                            href={jobsShow(retorno.id)}
                            className="text-primary font-medium underline underline-offset-4"
                        >
                            Ver la convocatoria
                        </Link>
                        <Link
                            href={jobsIndex()}
                            className="text-primary font-medium underline underline-offset-4"
                        >
                            Ver otras convocatorias
                        </Link>
                    </p>
                </AlertDescription>
            </Alert>
        );
    }

    return (
        <div
            className="bg-card flex flex-col gap-3 rounded-xl border p-4 sm:flex-row sm:items-center sm:justify-between"
            data-cy="profile-return"
        >
            <p className="text-sm [overflow-wrap:anywhere]">
                {ready
                    ? 'Su perfil está listo. Puede volver a la convocatoria '
                    : 'Cuando complete lo pendiente podrá volver a la convocatoria '}
                <span className="font-medium">{retorno.title}</span>
                {ready ? ' y decidir allí si postula.' : '.'}
            </p>
            {ready && (
                <Button asChild className="shrink-0">
                    <Link
                        href={jobsShow(retorno.id)}
                        data-cy="return-to-vacancy"
                    >
                        <ArrowLeft aria-hidden="true" />
                        Volver a la convocatoria
                    </Link>
                </Button>
            )}
        </div>
    );
}

export default function CandidateProfilePage({
    profile,
    cv,
    missingFields,
    educationLevels,
    cvMaxKb,
    retorno,
}: Props) {
    const pending = [...missingFields, ...(cv ? [] : ['CV en PDF'])];

    return (
        <>
            <Head title="Mi perfil" />
            <PageContainer className="max-w-5xl">
                <PageHeader
                    title="Mi perfil de postulante"
                    description="Mantenga actualizada su información y su CV para poder postular a las convocatorias."
                />

                {pending.length > 0 ? (
                    <Alert data-cy="profile-incomplete">
                        <AlertTriangle />
                        <AlertTitle>Falta completar su perfil</AlertTitle>
                        <AlertDescription>
                            Para postular necesita completar:{' '}
                            {pending.join(', ')}.
                        </AlertDescription>
                    </Alert>
                ) : (
                    <Alert data-cy="profile-complete">
                        <CheckCircle2 className="text-tone-success-foreground" />
                        <AlertTitle>Perfil listo para postular</AlertTitle>
                        <AlertDescription>
                            Su información y su CV están completos.
                        </AlertDescription>
                    </Alert>
                )}

                {retorno && (
                    <ReturnToVacancy
                        retorno={retorno}
                        ready={pending.length === 0}
                    />
                )}

                <div className="grid min-w-0 gap-6 lg:grid-cols-3">
                    <Section
                        title="Datos profesionales"
                        description="Solo se solicita la información necesaria para el proceso."
                        className="min-w-0 lg:col-span-2"
                    >
                        <Form
                            {...CandidateProfileController.update.form()}
                            options={{ preserveScroll: true }}
                            className="grid gap-5 md:grid-cols-2"
                        >
                            {({ errors, processing }) => (
                                <>
                                    <FormField
                                        label="Teléfono"
                                        htmlFor="phone"
                                        error={errors.phone}
                                    >
                                        <Input
                                            id="phone"
                                            name="phone"
                                            defaultValue={profile?.phone ?? ''}
                                            placeholder="9XXXXXXXX"
                                            data-cy="profile-phone"
                                        />
                                    </FormField>
                                    <FormField
                                        label="Ciudad"
                                        htmlFor="city"
                                        error={errors.city}
                                    >
                                        <Input
                                            id="city"
                                            name="city"
                                            defaultValue={profile?.city ?? ''}
                                            data-cy="profile-city"
                                        />
                                    </FormField>
                                    <FormField
                                        label="Nivel educativo"
                                        htmlFor="education_level"
                                        error={errors.education_level}
                                    >
                                        <NativeSelect
                                            id="education_level"
                                            name="education_level"
                                            options={educationLevels}
                                            placeholder="Seleccione…"
                                            defaultValue={
                                                profile?.education_level ?? ''
                                            }
                                            data-cy="profile-education-level"
                                        />
                                    </FormField>
                                    <FormField
                                        label="Años de experiencia"
                                        htmlFor="years_of_experience"
                                        error={errors.years_of_experience}
                                    >
                                        <Input
                                            id="years_of_experience"
                                            name="years_of_experience"
                                            type="number"
                                            min={0}
                                            max={60}
                                            defaultValue={
                                                profile?.years_of_experience ??
                                                ''
                                            }
                                            data-cy="profile-years"
                                        />
                                    </FormField>
                                    <FormField
                                        label="Título u ocupación"
                                        htmlFor="professional_title"
                                        error={errors.professional_title}
                                        className="md:col-span-2"
                                    >
                                        <Input
                                            id="professional_title"
                                            name="professional_title"
                                            defaultValue={
                                                profile?.professional_title ??
                                                ''
                                            }
                                            data-cy="profile-title"
                                        />
                                    </FormField>
                                    <FormField
                                        label="Resumen profesional"
                                        htmlFor="summary"
                                        error={errors.summary}
                                        hint="Opcional. Lo leerá quien revise su postulación."
                                        className="md:col-span-2"
                                    >
                                        <Textarea
                                            id="summary"
                                            name="summary"
                                            rows={4}
                                            defaultValue={
                                                profile?.summary ?? ''
                                            }
                                            data-cy="profile-summary"
                                        />
                                    </FormField>
                                    <div className="flex justify-end md:col-span-2">
                                        <Button
                                            type="submit"
                                            disabled={processing}
                                            data-cy="save-profile"
                                        >
                                            {processing && <Spinner />}
                                            Guardar perfil
                                        </Button>
                                    </div>
                                </>
                            )}
                        </Form>
                    </Section>

                    <Section
                        title="Currículum vitae"
                        description={`PDF de hasta ${Math.round(cvMaxKb / 1024)} MB. Se almacena de forma privada.`}
                        className="h-fit"
                    >
                        <div className="space-y-4">
                            {cv ? (
                                <a
                                    href={cv.download_url}
                                    className="hover:bg-surface flex items-center gap-3 rounded-lg border p-3 text-sm transition-colors"
                                    data-cy="current-cv"
                                >
                                    <FileText
                                        className="text-muted-foreground size-5 shrink-0"
                                        aria-hidden="true"
                                    />
                                    <span className="min-w-0">
                                        <span className="block truncate font-medium">
                                            {cv.original_name}
                                        </span>
                                        <span className="text-muted-foreground block text-xs">
                                            {formatFileSize(cv.size_bytes)},
                                            cargado el{' '}
                                            {formatDateTime(cv.uploaded_at)}
                                        </span>
                                    </span>
                                </a>
                            ) : (
                                <p
                                    className="text-muted-foreground text-sm"
                                    data-cy="no-cv"
                                >
                                    Todavía no ha cargado su CV.
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
                                        <Input
                                            type="file"
                                            name="cv"
                                            accept="application/pdf,.pdf"
                                            aria-label="Archivo PDF del CV"
                                            aria-invalid={
                                                errors.cv ? true : undefined
                                            }
                                            data-cy="cv-input"
                                        />
                                        <InputError message={errors.cv} />
                                        <Button
                                            type="submit"
                                            variant="outline"
                                            disabled={processing}
                                            className="w-full"
                                            data-cy="upload-cv"
                                        >
                                            {processing ? (
                                                <Spinner />
                                            ) : (
                                                <Upload aria-hidden="true" />
                                            )}
                                            {cv ? 'Reemplazar CV' : 'Cargar CV'}
                                        </Button>
                                    </>
                                )}
                            </Form>
                        </div>
                    </Section>
                </div>
            </PageContainer>
        </>
    );
}

CandidateProfilePage.layout = {
    breadcrumbs: [
        { title: 'Mi perfil', href: CandidateProfileController.edit() },
    ],
};
