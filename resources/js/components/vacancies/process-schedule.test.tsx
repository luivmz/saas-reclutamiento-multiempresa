import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, test } from 'vitest';
import {
    buildProcessSchedule,
    ProcessSchedule,
} from '@/components/vacancies/process-schedule';
import type { ScheduleInput } from '@/components/vacancies/process-schedule';

/**
 * Cronograma del proceso en el detalle de la vacante.
 *
 * Solo dibuja fechas que la vacante ya tiene registradas (GAP-01 incluido).
 * No estima nada: la estimación experimental es la tarjeta de ML-01, aparte.
 * Las horas van a las 15:00 UTC para que la fecha sea la misma en UTC y en Lima.
 */
const published: ScheduleInput = {
    status: { value: 'publicada', label: 'Publicada', tone: 'success' },
    opens_at: '2026-10-08',
    closes_at: '2026-10-28',
    target_completion_at: '2026-12-07T15:00:00Z',
    published_at: '2026-10-08T15:00:00Z',
    closed_at: null,
};

const states = (input: ScheduleInput, today: string) =>
    buildProcessSchedule(input, today).milestones.map((m) => [m.key, m.state]);

describe('buildProcessSchedule', () => {
    test('con un plazo no posterior a la publicación no dice que falte el plazo', () => {
        const input: ScheduleInput = {
            ...published,
            target_completion_at: '2026-10-08T15:00:00Z',
        };
        const pending = buildProcessSchedule(input, '2026-10-08');

        expect(pending.progress).toBeNull();
        expect(pending.summary).not.toContain('Sin plazo objetivo');
        expect(pending.summary).toContain('No se puede medir el avance');

        const overdue = buildProcessSchedule(input, '2026-10-12');

        expect(overdue.summary).toBe(
            'El plazo objetivo venció hace 4 días y el proceso sigue abierto.',
        );
    });

    test('un proceso cerrado sin fecha de cierre no muestra un plazo vencido ni un hito en curso', () => {
        const input: ScheduleInput = {
            ...published,
            status: { value: 'cerrada', label: 'Cerrada', tone: 'neutral' },
            closed_at: null,
        };
        const schedule = buildProcessSchedule(input, '2026-12-20');
        const target = schedule.milestones[2];

        expect(target.state).not.toBe('vencido');
        expect(target.detail).toBe('Sin fecha de cierre para comparar');
        expect(schedule.milestones.some((m) => m.current)).toBe(false);
        expect(schedule.summary).toBe('Proceso cerrado.');
    });

    test('en borrador, todo está previsto y el primer hito es el actual', () => {
        const draft: ScheduleInput = {
            ...published,
            status: { value: 'borrador', label: 'Borrador', tone: 'neutral' },
            published_at: null,
        };
        const schedule = buildProcessSchedule(draft, '2026-10-01');

        expect(states(draft, '2026-10-01')).toEqual([
            ['publicacion', 'actual'],
            ['postulaciones', 'pendiente'],
            ['plazo', 'pendiente'],
            ['cierre', 'pendiente'],
        ]);
        expect(schedule.milestones[0].detail).toBe('Prevista');
        expect(schedule.summary).toContain('todavía no está publicada');
        expect(schedule.progress).toBeNull();
    });

    test('con postulaciones abiertas, cuenta los días que quedan', () => {
        const schedule = buildProcessSchedule(published, '2026-10-23');

        expect(states(published, '2026-10-23')).toEqual([
            ['publicacion', 'completado'],
            ['postulaciones', 'actual'],
            ['plazo', 'pendiente'],
            ['cierre', 'pendiente'],
        ]);
        expect(schedule.milestones[1].detail).toBe('Quedan 5 días');
        expect(schedule.milestones[1].detail).not.toContain('1 días');
    });

    test('el último día de postulaciones se nombra así, y un día va en singular', () => {
        expect(
            buildProcessSchedule(published, '2026-10-28').milestones[1].detail,
        ).toBe('Último día');
        expect(
            buildProcessSchedule(published, '2026-10-27').milestones[1].detail,
        ).toBe('Queda 1 día');
    });

    test('escenario de la vacante 6: postulaciones cerradas y plazo en curso', () => {
        const schedule = buildProcessSchedule(published, '2026-11-07');

        expect(states(published, '2026-11-07')).toEqual([
            ['publicacion', 'completado'],
            ['postulaciones', 'completado'],
            ['plazo', 'actual'],
            ['cierre', 'pendiente'],
        ]);
        expect(schedule.milestones[2].detail).toBe('Faltan 30 días');
        expect(schedule.progress).toEqual({ day: 30, total: 60, percent: 50 });
        expect(schedule.summary).toBe('Día 30 de 60 del plazo objetivo.');
    });

    test('con el plazo vencido y el proceso abierto, el hito lo dice sin depender del color', () => {
        const schedule = buildProcessSchedule(published, '2026-12-10');
        const plazo = schedule.milestones[2];

        expect(plazo.state).toBe('vencido');
        expect(plazo.current).toBe(true);
        expect(plazo.detail).toBe('Vencido hace 3 días');
        expect(schedule.progress?.percent).toBe(100);
        expect(schedule.summary).toBe(
            'El plazo objetivo venció hace 3 días y el proceso sigue abierto.',
        );
    });

    test('cerrado dentro del plazo: todo completado y sin hito actual', () => {
        const closed: ScheduleInput = {
            ...published,
            status: { value: 'cerrada', label: 'Cerrada', tone: 'neutral' },
            closed_at: '2026-12-01T15:00:00Z',
        };
        const schedule = buildProcessSchedule(closed, '2026-12-20');

        expect(schedule.milestones.every((m) => m.state === 'completado')).toBe(
            true,
        );
        expect(schedule.milestones.some((m) => m.current)).toBe(false);
        expect(schedule.milestones[2].detail).toBe('Cumplido');
        expect(schedule.progress).toBeNull();
    });

    test('cerrado después del plazo: se registra como fuera de plazo', () => {
        const late: ScheduleInput = {
            ...published,
            status: { value: 'cerrada', label: 'Cerrada', tone: 'neutral' },
            closed_at: '2026-12-09T15:00:00Z',
        };
        const plazo = buildProcessSchedule(late, '2026-12-20').milestones[2];

        expect(plazo.state).toBe('fuera_de_plazo');
        expect(plazo.detail).toBe('Cerrado 2 días después del plazo');
    });

    test('sin plazo objetivo no inventa uno ni dibuja el avance', () => {
        const noTarget: ScheduleInput = {
            ...published,
            target_completion_at: null,
        };
        const schedule = buildProcessSchedule(noTarget, '2026-11-07');

        expect(schedule.milestones[2].detail).toBe(
            'Sin plazo objetivo registrado',
        );
        expect(schedule.progress).toBeNull();
        // Sin fecha, el plazo no puede ser el hito en curso: lo es el cierre.
        expect(schedule.milestones[2].current).toBe(false);
        expect(schedule.milestones[3]).toMatchObject({
            state: 'actual',
            current: true,
        });
    });

    test('un proceso cerrado sin plazo objetivo no tiene ningún hito en curso', () => {
        const closedNoTarget: ScheduleInput = {
            ...published,
            status: { value: 'cerrada', label: 'Cerrada', tone: 'neutral' },
            target_completion_at: null,
            closed_at: '2026-11-20T15:00:00Z',
        };

        expect(states(closedNoTarget, '2026-12-01')).toEqual([
            ['publicacion', 'completado'],
            ['postulaciones', 'completado'],
            ['plazo', 'pendiente'],
            ['cierre', 'completado'],
        ]);
        expect(
            buildProcessSchedule(closedNoTarget, '2026-12-01').milestones.some(
                (m) => m.current,
            ),
        ).toBe(false);
    });
});

describe('ProcessSchedule', () => {
    const markup = renderToStaticMarkup(
        <ProcessSchedule vacancy={published} today="2026-12-10" />,
    );

    test('es una lista ordenada con un único paso actual y el estado en texto', () => {
        expect(markup).toContain('data-cy="process-schedule"');
        expect(markup.match(/<ol[\s>]/g)).toHaveLength(1);
        expect(markup.match(/data-cy="process-milestone"/g)).toHaveLength(4);
        expect(markup.match(/aria-current="step"/g)).toHaveLength(1);
        // El estado se lee como texto, no solo como color.
        expect(markup).toContain('Estado: vencido');
        expect(markup).toContain('<time dateTime="2026-10-28"');
    });

    test('el vencido usa el token de peligro como texto, que cumple el contraste de la Fase 21', () => {
        expect(markup).toContain('text-tone-danger-foreground');
        expect(markup).not.toMatch(/text-tone-danger-foreground\/\d+/);
    });

    test('habla del proceso, nunca de personas ni de estimaciones', () => {
        const text = markup.replace(/<[^>]+>/g, ' ').toLowerCase();

        for (const word of [
            'candidat',
            'postulante',
            'puntaje',
            'ranking',
            'riesgo',
            'probabilidad',
            'recomend',
        ]) {
            expect(text).not.toContain(word);
        }
        expect(text).toContain('sin estimaciones');
    });
});
