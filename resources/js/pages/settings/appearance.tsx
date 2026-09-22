import { Head } from '@inertiajs/react';
import AppearanceTabs from '@/components/appearance-tabs';
import { Section } from '@/components/page';
import { edit as editAppearance } from '@/routes/appearance';

export default function Appearance() {
    return (
        <>
            <Head title="Apariencia" />

            <Section
                title="Apariencia"
                description="Elija el tema con el que verá la plataforma. La preferencia se guarda en este navegador."
            >
                <AppearanceTabs />
            </Section>
        </>
    );
}

Appearance.layout = {
    breadcrumbs: [{ title: 'Apariencia', href: editAppearance() }],
};
