import { Link } from '@inertiajs/react';
import {
    ArrowRight,
    BriefcaseBusiness,
    Check,
    ClipboardCheck,
    FileText,
    UserRound,
} from 'lucide-react';
import { useId, useState } from 'react';
import { ApplicationProcessScene } from '@/components/experience-3d/application-process-scene';
import type {
    ApplicationStep,
    LoadApplicationScene,
} from '@/components/experience-3d/application-scene-session';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { index as jobsIndex } from '@/routes/jobs';

const steps = [
    {
        id: 1,
        icon: BriefcaseBusiness,
        title: 'Elija una convocatoria',
        text: 'Revise el perfil del puesto, los criterios de evaluación y la fecha de cierre.',
    },
    {
        id: 2,
        icon: UserRound,
        title: 'Cree su cuenta de postulante',
        text: 'Regístrese con su nombre, correo y contraseña. Si ya tiene cuenta, inicie sesión.',
    },
    {
        id: 3,
        icon: FileText,
        title: 'Complete su perfil y cargue su CV',
        text: 'Abra Mi perfil y complete los datos que se indican en «Qué tener listo». Cargue allí su CV.',
    },
    {
        id: 4,
        icon: ClipboardCheck,
        title: 'Postule y siga su avance',
        text: 'Postule desde la convocatoria. Consulte la etapa en Mis postulaciones y los cambios en Notificaciones.',
    },
] as const;

export function ApplicationProcess({
    loadScene,
}: {
    loadScene?: LoadApplicationScene;
}) {
    const [selected, setSelected] = useState<ApplicationStep>(1);
    const current = steps[selected - 1];
    const descriptionId = useId();

    return (
        <div className="grid min-w-0 items-start gap-6 lg:grid-cols-[1fr_1fr] lg:gap-8">
            <div className="min-w-0">
                <ol
                    className="divide-border divide-y border-y"
                    aria-label="Pasos para postular"
                >
                    {steps.map((step) => {
                        const active = step.id === selected;

                        return (
                            <li key={step.id}>
                                <button
                                    type="button"
                                    aria-pressed={active}
                                    aria-controls={descriptionId}
                                    aria-describedby={
                                        active ? descriptionId : undefined
                                    }
                                    onClick={() => setSelected(step.id)}
                                    className="hover:bg-surface focus-visible:ring-ring aria-pressed:bg-tone-primary aria-pressed:text-tone-primary-foreground grid min-h-12 w-full grid-cols-[2rem_minmax(0,1fr)_1.25rem] items-center gap-2 px-3 py-2 text-left text-sm font-medium focus-visible:ring-2 focus-visible:ring-inset sm:gap-3 sm:text-base"
                                    data-cy="apply-step"
                                >
                                    <span className="bg-card flex size-8 items-center justify-center rounded-full border text-sm tabular-nums">
                                        {step.id}
                                    </span>
                                    <span>{step.title}</span>
                                    {active && (
                                        <Check
                                            aria-hidden="true"
                                            className="size-5"
                                        />
                                    )}
                                </button>
                            </li>
                        );
                    })}
                </ol>

                <p
                    id={descriptionId}
                    role="status"
                    aria-atomic="true"
                    className="text-muted-foreground mt-4 min-h-[4.5rem] text-sm leading-6 sm:min-h-12"
                    data-cy="apply-description"
                >
                    {current.text}
                </p>

                <Button
                    asChild
                    variant="outline"
                    className="mt-3 h-auto min-h-11 whitespace-normal"
                >
                    <Link href={jobsIndex()} data-cy="apply-jobs">
                        Ver convocatorias
                        <ArrowRight aria-hidden="true" />
                    </Link>
                </Button>
            </div>

            <ApplicationProcessScene
                step={selected}
                load={loadScene}
                onStepChange={setSelected}
                poster={<ProcessPoster selected={selected} />}
            />
        </div>
    );
}

function ProcessPoster({ selected }: { selected: ApplicationStep }) {
    return (
        <div
            className="grid aspect-[16/10] grid-cols-2 grid-rows-2 gap-3 p-4 sm:p-6 lg:gap-4 lg:p-7"
            data-cy="apply-poster"
        >
            {steps.map(({ id, icon: Icon }) => (
                <div
                    key={id}
                    data-active={selected === id}
                    className={cn(
                        'relative flex min-h-0 min-w-0 flex-col items-start justify-center gap-2 rounded-lg border p-3 sm:gap-3 sm:p-4',
                        selected === id
                            ? 'border-primary bg-primary text-primary-foreground shadow-sm'
                            : 'bg-card text-muted-foreground',
                    )}
                >
                    <Icon className="size-5 sm:size-8" />
                    <div className="w-full space-y-1.5">
                        <div className="h-1 w-3/4 rounded-full bg-current opacity-40" />
                        <div className="h-1 w-1/2 rounded-full bg-current opacity-25" />
                    </div>
                </div>
            ))}
        </div>
    );
}
