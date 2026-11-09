import { AlertTriangle, CheckCircle2, Circle, CircleDot } from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { Section } from '@/components/page';
import { calendarToday, formatDate, toCalendarDate } from '@/lib/format';
import { cn } from '@/lib/utils';
import type { Vacancy } from '@/types';

/**
 * Cronograma del proceso de una vacante.
 *
 * Dibuja solo fechas que la vacante ya tiene registradas: publicación, cierre de
 * postulaciones, plazo objetivo (GAP-01) y cierre del proceso. No estima nada:
 * la estimación experimental del proceso es la tarjeta de ML-01, que va aparte.
 */
export type ScheduleInput = Pick<
    Vacancy,
    | 'status'
    | 'opens_at'
    | 'closes_at'
    | 'target_completion_at'
    | 'published_at'
    | 'closed_at'
>;

export type MilestoneState =
    | 'completado'
    | 'actual'
    | 'pendiente'
    | 'vencido'
    | 'fuera_de_plazo';

export type Milestone = {
    key: 'publicacion' | 'postulaciones' | 'plazo' | 'cierre';
    label: string;
    date: string | null;
    state: MilestoneState;
    current: boolean;
    detail: string;
};

export type ProcessScheduleModel = {
    milestones: Milestone[];
    progress: { day: number; total: number; percent: number } | null;
    summary: string;
};

const DAY_MS = 86_400_000;

function dayNumber(calendarDate: string): number {
    const [year, month, day] = calendarDate.split('-').map(Number);

    return Date.UTC(year, month - 1, day) / DAY_MS;
}

function daysBetween(from: string, to: string): number {
    return dayNumber(to) - dayNumber(from);
}

function days(count: number): string {
    return `${count} ${count === 1 ? 'día' : 'días'}`;
}

const DONE: MilestoneState[] = ['completado', 'fuera_de_plazo'];

export function buildProcessSchedule(
    vacancy: ScheduleInput,
    today: string,
): ProcessScheduleModel {
    const status = vacancy.status.value;
    const isDraft = status === 'borrador';
    const isClosed = status === 'cerrada';
    const published = vacancy.published_at
        ? toCalendarDate(vacancy.published_at)
        : null;
    const closes = vacancy.closes_at ? toCalendarDate(vacancy.closes_at) : null;
    const target = vacancy.target_completion_at
        ? toCalendarDate(vacancy.target_completion_at)
        : null;
    const closed = vacancy.closed_at ? toCalendarDate(vacancy.closed_at) : null;

    const applicationsDone = isClosed || (closes !== null && today > closes);
    const remaining = closes ? daysBetween(today, closes) : null;

    let targetState: MilestoneState = 'pendiente';
    let targetDetail = 'Sin plazo objetivo registrado';

    if (target) {
        if (isClosed && closed) {
            const late = daysBetween(target, closed);
            targetState = late > 0 ? 'fuera_de_plazo' : 'completado';
            targetDetail =
                late > 0
                    ? `Cerrado ${days(late)} después del plazo`
                    : 'Cumplido';
        } else if (isClosed) {
            targetDetail = 'Sin fecha de cierre para comparar';
        } else if (today > target) {
            targetState = 'vencido';
            targetDetail = `Vencido hace ${days(daysBetween(target, today))}`;
        } else {
            targetDetail = `Faltan ${days(daysBetween(today, target))}`;
        }
    }

    const milestones: Milestone[] = [
        {
            key: 'publicacion',
            label: 'Publicación',
            date: vacancy.published_at ?? vacancy.opens_at,
            state: published ? 'completado' : 'pendiente',
            current: false,
            detail: published
                ? 'Publicada'
                : isDraft
                  ? 'Prevista'
                  : 'Pendiente',
        },
        {
            key: 'postulaciones',
            label: 'Cierre de postulaciones',
            date: vacancy.closes_at,
            state: applicationsDone && published ? 'completado' : 'pendiente',
            current: false,
            detail:
                applicationsDone && published
                    ? 'Postulaciones cerradas'
                    : remaining === null
                      ? 'Sin fecha registrada'
                      : remaining === 0
                        ? 'Último día'
                        : remaining > 0
                          ? `${remaining === 1 ? 'Queda' : 'Quedan'} ${days(remaining)}`
                          : 'Prevista',
        },
        {
            key: 'plazo',
            label: 'Plazo objetivo',
            date: vacancy.target_completion_at,
            state: targetState,
            current: false,
            detail: targetDetail,
        },
        {
            key: 'cierre',
            label: 'Cierre del proceso',
            date: vacancy.closed_at,
            state: isClosed ? 'completado' : 'pendiente',
            current: false,
            detail: isClosed ? 'Proceso cerrado' : 'Pendiente',
        },
    ];

    // El hito actual es el primero que no está hecho. Un plazo vencido sigue siéndolo;
    // un plazo sin fecha registrada no puede estar en curso, así que se salta. En un
    // proceso cerrado ya no hay hito en curso, aunque falte alguna fecha.
    const currentIndex = isClosed
        ? -1
        : milestones.findIndex(
              (m) => !DONE.includes(m.state) && !(m.key === 'plazo' && !target),
          );

    if (currentIndex >= 0) {
        const current = milestones[currentIndex];
        current.current = true;

        if (current.state === 'pendiente') {
            current.state = 'actual';
        }
    }

    let progress: ProcessScheduleModel['progress'] = null;
    let summary: string;

    if (isDraft) {
        summary =
            'La vacante todavía no está publicada; las fechas son las previstas.';
    } else if (isClosed) {
        summary = closed
            ? `Proceso cerrado el ${formatDate(closed)}.`
            : 'Proceso cerrado.';
    } else if (!target) {
        summary = 'Sin plazo objetivo registrado para medir el avance.';
    } else {
        if (published && dayNumber(target) > dayNumber(published)) {
            const total = daysBetween(published, target);
            const day = Math.min(
                Math.max(daysBetween(published, today), 0),
                total,
            );
            progress = { day, total, percent: Math.round((day / total) * 100) };
        }

        summary =
            targetState === 'vencido'
                ? `El plazo objetivo venció hace ${days(daysBetween(target, today))} y el proceso sigue abierto.`
                : progress
                  ? `Día ${progress.day} de ${progress.total} del plazo objetivo.`
                  : 'No se puede medir el avance con las fechas registradas.';
    }

    return { milestones, progress, summary };
}

const presentation: Record<
    MilestoneState,
    { icon: LucideIcon; marker: string; text: string; label: string }
> = {
    completado: {
        icon: CheckCircle2,
        marker: 'bg-tone-success text-tone-success-foreground ring-tone-success-edge',
        text: 'text-tone-success-foreground',
        label: 'completado',
    },
    actual: {
        icon: CircleDot,
        marker: 'bg-tone-primary text-tone-primary-foreground ring-tone-primary-edge',
        text: 'text-tone-primary-foreground',
        label: 'en curso',
    },
    pendiente: {
        icon: Circle,
        marker: 'bg-tone-neutral text-tone-neutral-foreground ring-tone-neutral-edge',
        text: 'text-muted-foreground',
        label: 'pendiente',
    },
    vencido: {
        icon: AlertTriangle,
        marker: 'bg-tone-danger text-tone-danger-foreground ring-tone-danger-edge',
        text: 'text-tone-danger-foreground',
        label: 'vencido',
    },
    fuera_de_plazo: {
        icon: AlertTriangle,
        marker: 'bg-tone-warning text-tone-warning-foreground ring-tone-warning-edge',
        text: 'text-tone-warning-foreground',
        label: 'fuera de plazo',
    },
};

const progressTone: Record<MilestoneState, string> = {
    completado: 'bg-tone-success-foreground',
    actual: 'bg-tone-primary-foreground',
    pendiente: 'bg-tone-primary-foreground',
    vencido: 'bg-tone-danger-foreground',
    fuera_de_plazo: 'bg-tone-warning-foreground',
};

export function ProcessSchedule({
    vacancy,
    today,
}: {
    vacancy: ScheduleInput;
    /** Día de referencia (YYYY-MM-DD); por defecto, hoy en la zona horaria de la aplicación. */
    today?: string;
}) {
    const schedule = buildProcessSchedule(vacancy, today ?? calendarToday());
    const target = schedule.milestones[2];

    return (
        <Section
            title="Cronograma del proceso"
            description="Fechas registradas de la convocatoria, sin estimaciones."
            data-cy="process-schedule"
        >
            <ol
                aria-label="Hitos del proceso"
                className="grid gap-x-4 gap-y-5 sm:grid-cols-4"
            >
                {schedule.milestones.map((milestone, index) => {
                    const look = presentation[milestone.state];
                    const Icon = look.icon;

                    return (
                        <li
                            key={milestone.key}
                            data-cy="process-milestone"
                            data-milestone={milestone.key}
                            data-state={milestone.state}
                            aria-current={
                                milestone.current ? 'step' : undefined
                            }
                            className="relative flex min-w-0 gap-3 sm:flex-col sm:gap-2.5"
                        >
                            {/* Conector con el hito siguiente: vertical en móvil, horizontal desde sm. */}
                            {index < schedule.milestones.length - 1 && (
                                <span
                                    aria-hidden="true"
                                    className="bg-border absolute top-8 bottom-[-1.25rem] left-[0.9375rem] w-px sm:top-[0.9375rem] sm:right-[-1rem] sm:bottom-auto sm:left-9 sm:h-px sm:w-auto"
                                />
                            )}
                            <span
                                aria-hidden="true"
                                className={cn(
                                    'relative z-10 flex size-[1.875rem] shrink-0 items-center justify-center rounded-full ring-1 ring-inset',
                                    look.marker,
                                    milestone.current &&
                                        'ring-offset-card ring-2 ring-offset-2',
                                )}
                            >
                                <Icon className="size-4" />
                            </span>
                            <div className="min-w-0 space-y-0.5">
                                <p className="text-sm font-medium">
                                    {milestone.label}
                                </p>
                                <p className="text-muted-foreground text-xs">
                                    {milestone.date ? (
                                        <time
                                            dateTime={toCalendarDate(
                                                milestone.date,
                                            )}
                                        >
                                            {formatDate(milestone.date)}
                                        </time>
                                    ) : (
                                        'Sin fecha'
                                    )}
                                </p>
                                <p
                                    className={cn(
                                        'text-xs font-medium',
                                        look.text,
                                    )}
                                >
                                    <span className="sr-only">
                                        Estado: {look.label}.{' '}
                                    </span>
                                    {milestone.detail}
                                </p>
                            </div>
                        </li>
                    );
                })}
            </ol>

            <div className="mt-6 space-y-2" data-cy="process-schedule-progress">
                {schedule.progress && (
                    <div
                        aria-hidden="true"
                        className="bg-muted h-1.5 overflow-hidden rounded-full"
                    >
                        <div
                            className={cn(
                                'h-full rounded-full',
                                progressTone[target.state],
                            )}
                            style={{ width: `${schedule.progress.percent}%` }}
                        />
                    </div>
                )}
                <p
                    className="text-muted-foreground text-xs"
                    data-cy="process-schedule-summary"
                >
                    {schedule.summary}
                </p>
            </div>
        </Section>
    );
}
