import { Form, Head, Link } from '@inertiajs/react';
import { Bell, CheckCheck } from 'lucide-react';
import NotificationController from '@/actions/App/Http/Controllers/NotificationController';
import { EmptyState } from '@/components/empty-state';
import { PageContainer, PageHeader } from '@/components/page';
import { Pagination } from '@/components/pagination';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { formatDateTime } from '@/lib/format';
import { cn } from '@/lib/utils';
import type { AppNotification, Paginated } from '@/types';

export default function NotificationsIndex({
    notifications,
}: {
    notifications: Paginated<AppNotification>;
}) {
    const hasUnread = notifications.data.some((notification) => !notification.read_at);

    return (
        <>
            <Head title="Notificaciones" />
            <PageContainer className="max-w-3xl">
                <PageHeader
                    title="Notificaciones"
                    description="Avisos generados por el proceso de reclutamiento."
                    actions={
                        hasUnread && (
                            <Form {...NotificationController.markAllAsRead.form()}>
                                {({ processing }) => (
                                    <Button variant="outline" type="submit" disabled={processing} data-cy="mark-all-read">
                                        <CheckCheck />
                                        Marcar todas como leídas
                                    </Button>
                                )}
                            </Form>
                        )
                    }
                />
                {notifications.data.length === 0 ? (
                    <EmptyState icon={Bell} title="No tiene notificaciones" description="Aquí verá los avisos sobre sus procesos." />
                ) : (
                    <Card className="gap-0 divide-y py-0" data-cy="notifications-list">
                        {notifications.data.map((notification) => (
                            <div
                                key={notification.id}
                                className={cn('flex gap-3 p-4', !notification.read_at && 'bg-primary/5')}
                                data-cy="notification-item"
                                data-kind={notification.kind}
                                data-read={notification.read_at ? 'true' : 'false'}
                            >
                                <span className={cn('mt-2 size-2 shrink-0 rounded-full', notification.read_at ? 'bg-transparent' : 'bg-primary')} />
                                <div className="min-w-0 flex-1 space-y-1">
                                    <p className="font-medium">{notification.title}</p>
                                    <p className="text-muted-foreground text-sm">{notification.message}</p>
                                    <p className="text-muted-foreground text-xs">{formatDateTime(notification.created_at)}</p>
                                </div>
                                {(notification.url || !notification.read_at) && (
                                    <Link
                                        href={NotificationController.markAsRead(notification.id)}
                                        as="button"
                                        className="self-start text-sm font-medium hover:underline"
                                        data-cy="open-notification"
                                    >
                                        {notification.url ? 'Ver' : 'Marcar leída'}
                                    </Link>
                                )}
                            </div>
                        ))}
                    </Card>
                )}
                <Pagination meta={notifications.meta} />
            </PageContainer>
        </>
    );
}

NotificationsIndex.layout = {
    breadcrumbs: [{ title: 'Notificaciones', href: NotificationController.index() }],
};
