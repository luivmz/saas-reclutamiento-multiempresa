import { Link } from '@inertiajs/react';
import type { PropsWithChildren } from 'react';
import { PageContainer, PageHeader } from '@/components/page';
import { useCurrentUrl } from '@/hooks/use-current-url';
import { cn, toUrl } from '@/lib/utils';
import { edit as editAppearance } from '@/routes/appearance';
import { edit } from '@/routes/profile';
import { edit as editSecurity } from '@/routes/security';
import type { NavItem } from '@/types';

/**
 * Configuración de la cuenta.
 *
 * Venía del kit de inicio de Laravel y era la única zona de la aplicación en
 * inglés. Ahora habla el mismo idioma que el resto y usa el encabezado de
 * página común, para que no parezca otro producto.
 */
const sections: NavItem[] = [
    { title: 'Perfil', href: edit(), icon: null },
    { title: 'Seguridad', href: editSecurity(), icon: null },
    { title: 'Apariencia', href: editAppearance(), icon: null },
];

export default function SettingsLayout({ children }: PropsWithChildren) {
    const { isCurrentOrParentUrl } = useCurrentUrl();

    return (
        <PageContainer className="max-w-5xl">
            <PageHeader
                title="Configuración de la cuenta"
                description="Sus datos de acceso y sus preferencias. No afecta a los expedientes ni a los procesos de su organización."
            />

            <div className="grid gap-8 lg:grid-cols-[13rem_minmax(0,1fr)]">
                <nav aria-label="Secciones de configuración">
                    <ul className="flex flex-wrap gap-1 lg:flex-col">
                        {sections.map((section) => {
                            const isCurrent = isCurrentOrParentUrl(
                                section.href,
                            );

                            return (
                                <li key={toUrl(section.href)}>
                                    <Link
                                        href={section.href}
                                        aria-current={
                                            isCurrent ? 'page' : undefined
                                        }
                                        className={cn(
                                            'hover:bg-surface block rounded-md px-3 py-2 text-sm transition-colors',
                                            isCurrent &&
                                                'bg-surface text-foreground font-medium',
                                        )}
                                    >
                                        {section.title}
                                    </Link>
                                </li>
                            );
                        })}
                    </ul>
                </nav>

                <div className="min-w-0 space-y-8">{children}</div>
            </div>
        </PageContainer>
    );
}
