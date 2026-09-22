import { StatusBadge } from '@/components/status-badge';
import { formatNumber } from '@/lib/format';
import type { Criterion } from '@/types';

/**
 * Criterios de una vacante con su ponderación y su escala.
 *
 * Es una tabla corta y fija, no un listado paginado, así que no usa
 * `DataTable`: aquí lo que importa es que la suma del pie quede pegada a las
 * ponderaciones que la componen.
 */
export function CriteriaTable({ criteria }: { criteria: Criterion[] }) {
    const total = criteria.reduce(
        (sum, criterion) => sum + criterion.weight,
        0,
    );

    if (criteria.length === 0) {
        return (
            <p className="text-muted-foreground text-sm">
                Todavía no hay criterios configurados.
            </p>
        );
    }

    return (
        <div className="overflow-x-auto">
            <table className="w-full text-sm" data-cy="criteria-table">
                <caption className="sr-only">
                    Criterios de evaluación, con su etapa, su ponderación y su
                    escala de puntaje
                </caption>
                <thead className="text-muted-foreground border-b text-left text-xs">
                    <tr>
                        <th scope="col" className="py-2 pr-4 font-medium">
                            Criterio
                        </th>
                        <th scope="col" className="py-2 pr-4 font-medium">
                            Etapa
                        </th>
                        <th
                            scope="col"
                            className="py-2 pr-4 text-right font-medium"
                        >
                            Ponderación
                        </th>
                        <th scope="col" className="py-2 text-right font-medium">
                            Escala
                        </th>
                    </tr>
                </thead>
                <tbody className="divide-y">
                    {criteria.map((criterion) => (
                        <tr key={criterion.id}>
                            <th
                                scope="row"
                                className="py-2.5 pr-4 text-left font-medium"
                            >
                                {criterion.name}
                            </th>
                            <td className="py-2.5 pr-4">
                                <StatusBadge status={criterion.stage} />
                            </td>
                            <td className="py-2.5 pr-4 text-right font-mono tabular-nums">
                                {formatNumber(criterion.weight)}
                            </td>
                            <td className="text-muted-foreground py-2.5 text-right font-mono tabular-nums">
                                {formatNumber(criterion.min_score)} –{' '}
                                {formatNumber(criterion.max_score)}
                            </td>
                        </tr>
                    ))}
                </tbody>
                <tfoot className="border-t">
                    <tr>
                        <th
                            scope="row"
                            colSpan={2}
                            className="py-2.5 pr-4 text-left font-medium"
                        >
                            Total
                        </th>
                        <td
                            className="py-2.5 pr-4 text-right font-mono font-medium tabular-nums"
                            data-cy="criteria-total"
                        >
                            {formatNumber(total)}
                        </td>
                        <td />
                    </tr>
                </tfoot>
            </table>
        </div>
    );
}
