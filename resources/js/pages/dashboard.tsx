import { Head, Link, usePage } from '@inertiajs/react';
import { ArrowRight, ShieldCheck } from 'lucide-react';
import { PageContainer, PageHeader } from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import { navigationFor } from '@/lib/navigation';
import { dashboard } from '@/routes';

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
                            ? `Organización: ${auth.organization.name}`
                            : 'Portal de postulantes'
                    }
                />

                <div
                    className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
                    data-cy="quick-links"
                >
                    {links.map((link) => (
                        <Link key={link.title} href={link.href} className="group">
                            <Card className="group-hover:border-primary/40 h-full gap-3 transition-colors">
                                <CardHeader className="gap-2">
                                    <div className="flex items-center justify-between">
                                        {link.icon && (
                                            <link.icon className="text-muted-foreground size-5" />
                                        )}
                                        <ArrowRight className="text-muted-foreground size-4 transition-transform group-hover:translate-x-0.5" />
                                    </div>
                                    <CardTitle className="text-base">
                                        {link.title}
                                    </CardTitle>
                                    <CardDescription>
                                        {link.description}
                                    </CardDescription>
                                </CardHeader>
                            </Card>
                        </Link>
                    ))}
                </div>

                <Card className="bg-muted/30 border-dashed">
                    <CardContent className="flex gap-3 text-sm">
                        <ShieldCheck className="size-5 shrink-0 text-emerald-600" />
                        <p>
                            El sistema calcula puntajes y rankings como apoyo.{' '}
                            <strong>
                                La decisión final de selección siempre la registra
                                una persona autorizada
                            </strong>{' '}
                            (RF-23).
                        </p>
                    </CardContent>
                </Card>
            </PageContainer>
        </>
    );
}

Dashboard.layout = {
    breadcrumbs: [{ title: 'Panel', href: dashboard() }],
};
