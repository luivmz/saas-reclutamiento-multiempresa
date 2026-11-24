import { FileText, UserRound } from 'lucide-react';
import type { ApplicationRequirements as Requirements } from '@/types';

/** «a, b y c»: enumeración en castellano. */
export function joinList(items: string[]): string {
    if (items.length <= 1) {
        return items.join('');
    }

    return `${items.slice(0, -1).join(', ')} y ${items[items.length - 1]}`;
}

/** 5120 KB → «5 MB»; si no es un número entero de megabytes, en KB. */
export function formatCvLimit(kb: number): string {
    return kb % 1024 === 0 ? `${kb / 1024} MB` : `${kb} KB`;
}

/**
 * Lo que pide toda postulación: el perfil y el CV. Sale de las mismas reglas
 * que valida el servidor, así que nunca anuncia algo distinto de lo que se
 * exige. Los requisitos propios de cada puesto están en su convocatoria.
 */
export function ApplicationRequirements({
    requirements,
    compact = false,
}: {
    requirements: Requirements;
    compact?: boolean;
}) {
    const perfil = joinList(requirements.perfil);
    const cv = `un archivo ${requirements.cv.formato} de hasta ${formatCvLimit(requirements.cv.max_kb)}`;

    if (compact) {
        return (
            <p
                className="text-muted-foreground text-sm leading-relaxed"
                data-cy="application-requirements"
            >
                Para postular, su perfil debe incluir {perfil}, y debe cargar su
                CV en {cv}.
            </p>
        );
    }

    return (
        <ul className="space-y-4 text-sm" data-cy="application-requirements">
            <li className="flex items-start gap-3">
                <UserRound
                    className="text-primary mt-0.5 size-4 shrink-0"
                    aria-hidden="true"
                />
                <p className="leading-relaxed">
                    <span className="font-medium">Su perfil de postulante</span>
                    <span className="text-muted-foreground">
                        {' '}
                        con {perfil}. El resumen profesional es opcional.
                    </span>
                </p>
            </li>
            <li className="flex items-start gap-3">
                <FileText
                    className="text-primary mt-0.5 size-4 shrink-0"
                    aria-hidden="true"
                />
                <p className="leading-relaxed">
                    <span className="font-medium">Su CV</span>
                    <span className="text-muted-foreground"> en {cv}.</span>
                </p>
            </li>
        </ul>
    );
}
