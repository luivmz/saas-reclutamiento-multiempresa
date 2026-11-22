import type { JSX } from 'react';
import { cn } from '@/lib/utils';

/**
 * Las tres hojas detrás del expediente: vacante, evidencias y decisión humana.
 *
 * Son el mismo recorrido que el expediente cuenta con palabras, dicho con
 * formas: una ficha de convocatoria con sus criterios, un legajo de evidencias
 * versionadas y una hoja de firma. No llevan texto ni cifras —todo lo que la
 * portada dice está en el expediente de delante, que es DOM normal—; son
 * pictogramas hechos con cajas, sin imágenes ni dependencias.
 *
 * El póster (plano) y la escena (en profundidad) pintan las mismas hojas, así
 * que cambiar uno por otra no cambia lo que se cuenta.
 */

export type SheetKind = 'vacancy' | 'evidence' | 'decision';

/** Del fondo hacia el frente. Mismos tonos que el expediente. */
export const STAGE_SHEETS = [
    { stage: 'vacancy', edge: 'bg-tone-primary-edge' },
    { stage: 'evidence', edge: 'bg-tone-info-edge' },
    { stage: 'decision', edge: 'bg-tone-success-edge' },
] as const satisfies readonly { stage: SheetKind; edge: string }[];

function Bar({ className }: { className: string }) {
    return (
        <span className={cn('bg-border block h-1.5 rounded-full', className)} />
    );
}

/** Ficha de convocatoria: cabecera y tres criterios ponderados. */
function VacancyGlyph() {
    return (
        <span className="absolute top-6 left-6 flex w-40 flex-col gap-2.5">
            <span className="flex items-center gap-2">
                <span className="bg-tone-primary ring-tone-primary-edge size-7 rounded-md ring-1" />
                <Bar className="w-20" />
            </span>
            {[0.85, 0.6, 0.45].map((weight) => (
                <span key={weight} className="flex items-center gap-2">
                    <Bar className="w-14" />
                    <span
                        className="bg-tone-primary-edge block h-1.5 rounded-full"
                        style={{ width: `${weight * 72}px` }}
                    />
                </span>
            ))}
        </span>
    );
}

/** Legajo de evidencias: la versión vigente sobre la anterior, conservada. */
function EvidenceGlyph() {
    return (
        <span className="absolute top-6 right-6 block h-20 w-40">
            <span className="border-tone-info-edge bg-surface absolute top-0 right-4 block h-14 w-32 rounded-md border border-dashed" />
            <span className="bg-card ring-tone-info-edge absolute top-4 right-0 flex h-14 w-32 flex-col gap-1.5 rounded-md p-2.5 shadow-sm ring-1">
                <Bar className="w-16" />
                <Bar className="w-24" />
                <span className="bg-tone-info-edge block h-1.5 w-9 rounded-full" />
            </span>
        </span>
    );
}

/** Hoja de firma: la decisión la registra una persona. */
function DecisionGlyph() {
    return (
        <span className="absolute right-6 bottom-6 flex w-44 flex-col items-end gap-2">
            <span className="bg-tone-success ring-tone-success-edge flex size-8 items-center justify-center rounded-full ring-1">
                <span className="border-tone-success-foreground block h-2 w-3.5 -translate-y-0.5 -rotate-45 border-b-2 border-l-2" />
            </span>
            <svg
                viewBox="0 0 120 24"
                className="text-tone-success-foreground/70 h-6 w-32"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
            >
                <path d="M2 18c10-14 16-14 18-2s8 4 14-6 10-6 12 4 10 6 18-4 14-4 18 2 12 6 20-2" />
            </svg>
            <Bar className="w-36" />
        </span>
    );
}

const GLYPHS: Record<SheetKind, () => JSX.Element> = {
    vacancy: VacancyGlyph,
    evidence: EvidenceGlyph,
    decision: DecisionGlyph,
};

/**
 * Una hoja sin texto. El tono de su etapa va en la pestaña de arriba; el
 * pictograma, en la esquina que asoma detrás del expediente. Una veladura de
 * luz desde arriba a la izquierda da a todas la misma iluminación.
 */
export function SheetFace({ edge, kind }: { edge: string; kind?: SheetKind }) {
    const Glyph = kind ? GLYPHS[kind] : null;

    return (
        <>
            <span
                className={cn(
                    'absolute inset-x-0 top-0 h-[3px] rounded-t-xl',
                    edge,
                )}
            />
            <span className="absolute inset-0 rounded-[inherit] bg-gradient-to-br from-white/70 via-white/0 to-transparent dark:from-white/[0.06]" />
            {Glyph ? (
                <Glyph />
            ) : (
                <span className="bg-border absolute top-2.5 left-5 h-1 w-16 rounded-full" />
            )}
        </>
    );
}

/**
 * Lo que se ve al instante y lo que queda cuando la escena no procede:
 * movimiento reducido, pantalla angosta, ahorro de datos, equipo modesto o una
 * escena que no cargó. Las hojas asoman solo por arriba y siempre dentro del
 * ancho de la tarjeta: a 320 px no pueden empujar la página en horizontal.
 */
export function RecruitmentScenePoster() {
    return (
        <div className="absolute inset-0" data-cy="recruitment-poster">
            {STAGE_SHEETS.map((sheet, index) => {
                // Del fondo (3) al frente (1): cada hoja asoma un poco menos.
                const depth = STAGE_SHEETS.length - index;

                return (
                    <div
                        key={sheet.stage}
                        className="bg-card absolute overflow-hidden rounded-xl border shadow-sm"
                        style={{
                            inset: `0 ${depth * 12}px`,
                            transform: `translateY(-${depth * 10}px)`,
                            opacity: 1 - depth * 0.16,
                        }}
                    >
                        <SheetFace edge={sheet.edge} />
                    </div>
                );
            })}
        </div>
    );
}
