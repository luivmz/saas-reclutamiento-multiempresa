import { StatusBadge } from '@/components/status-badge';
import { formatNumber } from '@/lib/format';
import type { Criterion } from '@/types';

export function CriteriaTable({ criteria }: { criteria: Criterion[] }) {
    const total = criteria.reduce((sum, criterion) => sum + criterion.weight, 0);

    if (criteria.length === 0) {
        return (
            <p className="text-muted-foreground text-sm">
                No hay criterios configurados.
            </p>
        );
    }

    return (
        <div className="overflow-x-auto">
            <table className="w-full text-sm" data-cy="criteria-table">
                <thead className="text-muted-foreground border-b text-left text-xs tracking-wide uppercase">
                    <tr>
                        <th className="py-2 pr-4 font-medium">Criterio</th>
                        <th className="py-2 pr-4 font-medium">Etapa</th>
                        <th className="py-2 pr-4 text-right font-medium">Ponderación</th>
                        <th className="py-2 text-right font-medium">Rango</th>
                    </tr>
                </thead>
                <tbody className="divide-y">
                    {criteria.map((criterion) => (
                        <tr key={criterion.id}>
                            <td className="py-2 pr-4 font-medium">{criterion.name}</td>
                            <td className="py-2 pr-4">
                                <StatusBadge status={criterion.stage} />
                            </td>
                            <td className="py-2 pr-4 text-right tabular-nums">
                                {formatNumber(criterion.weight)}
                            </td>
                            <td className="text-muted-foreground py-2 text-right tabular-nums">
                                {formatNumber(criterion.min_score)} – {formatNumber(criterion.max_score)}
                            </td>
                        </tr>
                    ))}
                </tbody>
                <tfoot className="border-t">
                    <tr>
                        <td className="py-2 pr-4 font-medium" colSpan={2}>
                            Total
                        </td>
                        <td className="py-2 pr-4 text-right font-semibold tabular-nums" data-cy="criteria-total">
                            {formatNumber(total)}
                        </td>
                        <td />
                    </tr>
                </tfoot>
            </table>
        </div>
    );
}
