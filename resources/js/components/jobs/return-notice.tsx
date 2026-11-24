import { BriefcaseBusiness } from 'lucide-react';
import type { ChosenVacancy } from '@/types';

/**
 * Avisa, en el acceso y el registro, a qué convocatoria se volverá después.
 * En el acceso se precisa que es con una cuenta de postulante: los demás
 * roles van a su panel.
 */
export function ReturnNotice({
    vacancy,
    context,
}: {
    vacancy: ChosenVacancy;
    context: 'login' | 'register';
}) {
    return (
        <p
            className="bg-surface flex items-start gap-2.5 rounded-md border px-3 py-2.5 text-sm"
            data-cy="return-notice"
        >
            <BriefcaseBusiness
                className="text-primary mt-0.5 size-4 shrink-0"
                aria-hidden="true"
            />
            <span>
                {context === 'login'
                    ? 'Si entra con una cuenta de postulante, volverá a la convocatoria '
                    : 'Al crear su cuenta volverá a la convocatoria '}
                <span className="font-medium [overflow-wrap:anywhere]">
                    {vacancy.title}
                </span>
                . Allí decidirá si postula.
            </span>
        </p>
    );
}
