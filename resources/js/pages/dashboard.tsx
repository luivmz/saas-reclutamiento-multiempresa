import { Head, Link, usePage } from '@inertiajs/react';
import { ShieldCheck } from 'lucide-react';
import { PageContainer, PageHeader } from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import { navigationFor } from '@/lib/navigation';
import { dashboard } from '@/routes';

/**
 * Panel de inicio.
 *
 * No inventa métricas: muestra exactamente lo que esta persona puede hacer
 * según su rol y para qué sirve cada cosa. Se presenta como un índice con
 * renglones, no como una parrilla de tarjetas iguales, porque eso es lo que
 * es: la portada de un expediente.
 */
export default function Dashboard() {
    const { auth } = usePage().props;
    const links = navigationFor(auth.user.role)
        .flatMap((group) => group.items)
        .filter((item) => item.cy !== 'dashboard');

    return (
        <>
            <Head title="Panel" />
            <PageContainer>
                <PageHeader
                    eyebrow={auth.role && <StatusBadge status={auth.role} />}
                    title={`Hola, ${auth.user.name}`}
                    description={
                        auth.organization
                            ? `Está trabajando en ${auth.organization.name}. Estas son las secciones que su rol tiene habilitadas.`
                            : 'Portal de postulantes. Estas son las secciones disponibles para su cuenta.'
                    }
                />

                <ul
                    className="bg-card divide-y overflow-hidden rounded-xl border"
                    data-cy="quick-links"
                >
                    {links.map((link) => (
                        <li key={link.title}>
                            <Link
                                href={link.href}
                                className="hover:bg-surface flex items-start gap-4 px-5 py-4 transition-colors"
                            >
                                {link.icon && (
                                    <span className="bg-surface text-primary mt-0.5 flex size-9 shrink-0 items-center justify-center rounded-md">
                                        <link.icon
                                            className="size-4"
                                            aria-hidden="true"
                                        />
                                    </span>
                                )}
                                <span className="min-w-0 space-y-1">
                                    <span className="block font-medium">
                                        {link.title}
                                    </span>
                                    <span className="text-muted-foreground block text-sm leading-relaxed">
                                        {link.description}
                                    </span>
                                </span>
                                {link.badge ? (
                                    <span className="bg-primary text-primary-foreground ml-auto rounded-full px-2 py-0.5 text-xs font-semibold">
                                        {link.badge}
                                        <span className="sr-only">
                                            {' '}
                                            sin leer
                                        </span>
                                    </span>
                                ) : null}
                            </Link>
                        </li>
                    ))}
                </ul>

                <aside className="bg-surface text-surface-foreground flex gap-3 rounded-xl border border-dashed px-5 py-4 text-sm leading-relaxed">
                    <ShieldCheck
                        className="text-primary mt-0.5 size-5 shrink-0"
                        aria-hidden="true"
                    />
                    <p>
                        El sistema calcula puntajes y rankings como apoyo.{' '}
                        <strong className="font-medium">
                            La decisión final de selección siempre la registra
                            una persona autorizada
                        </strong>{' '}
                        (RF-23).
                    </p>
                </aside>
            </PageContainer>
        </>
    );
}

Dashboard.layout = {
    breadcrumbs: [{ title: 'Panel', href: dashboard() }],
};
