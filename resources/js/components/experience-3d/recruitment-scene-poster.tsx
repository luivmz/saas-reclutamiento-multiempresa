import { cn } from '@/lib/utils';

/**
 * El archivo detrás del expediente, en plano.
 *
 * Es lo que se ve al instante y lo que queda para siempre cuando la escena no
 * procede: movimiento reducido, pantalla angosta, ahorro de datos, equipo
 * modesto, o una escena que no cargó. Cuenta lo mismo que la escena —el
 * expediente de la portada es uno entre muchos, cada uno en su etapa— sin
 * perspectiva ni movimiento.
 *
 * Las hojas asoman solo por arriba y siempre dentro del ancho de la tarjeta:
 * a 390 px no pueden empujar la página en horizontal.
 */

/** Etapas del proceso, del fondo hacia el frente. Mismos tonos que la portada. */
export const STAGE_SHEETS = [
    { stage: 'Requerimiento', edge: 'bg-tone-neutral-edge' },
    { stage: 'Validación', edge: 'bg-tone-info-edge' },
    { stage: 'Aprobación', edge: 'bg-tone-success-edge' },
    { stage: 'Convocatoria', edge: 'bg-tone-primary-edge' },
] as const;

/**
 * Una hoja de expediente sin contenido. De cada hoja solo asoma la franja de
 * arriba, así que el tono de su etapa va en ese borde, como la pestaña de una
 * carpeta, y debajo un renglón, como los de la marca.
 */
export function SheetFace({ edge }: { edge: string }) {
    return (
        <>
            <span
                className={cn(
                    'absolute inset-x-0 top-0 h-[3px] rounded-t-xl',
                    edge,
                )}
            />
            <span className="bg-border absolute top-2.5 left-5 h-1 w-16 rounded-full" />
        </>
    );
}

export function RecruitmentScenePoster() {
    return (
        <div className="absolute inset-0" data-cy="recruitment-poster">
            {STAGE_SHEETS.map((sheet, index) => {
                // Del fondo (0) al frente (3): cada hoja asoma un poco menos.
                const depth = STAGE_SHEETS.length - index;

                return (
                    <div
                        key={sheet.stage}
                        className="bg-card absolute rounded-xl border"
                        style={{
                            inset: `0 ${depth * 12}px`,
                            transform: `translateY(-${depth * 9}px)`,
                            opacity: 1 - depth * 0.15,
                        }}
                    >
                        <SheetFace edge={sheet.edge} />
                    </div>
                );
            })}
        </div>
    );
}
