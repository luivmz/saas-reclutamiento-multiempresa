import { AppContent } from '@/components/app-content';
import { AppShell } from '@/components/app-shell';
import { AppSidebar } from '@/components/app-sidebar';
import { AppSidebarHeader } from '@/components/app-sidebar-header';
import { MAIN_CONTENT_ID, SkipLink } from '@/components/skip-link';
import type { AppLayoutProps } from '@/types';

export default function AppSidebarLayout({
    children,
    breadcrumbs = [],
}: AppLayoutProps) {
    return (
        <AppShell variant="sidebar">
            <SkipLink />
            <AppSidebar />
            <AppContent variant="sidebar" className="min-w-0 overflow-x-clip">
                <AppSidebarHeader breadcrumbs={breadcrumbs} />
                {/* `tabIndex={-1}` para que el salto al contenido deje el foco
                    aquí y la siguiente tabulación siga dentro de la página. */}
                <div id={MAIN_CONTENT_ID} tabIndex={-1} className="flex-1">
                    {children}
                </div>
            </AppContent>
        </AppShell>
    );
}
