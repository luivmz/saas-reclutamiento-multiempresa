import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, test } from 'vitest';
import { SidebarMenuSkeleton } from '@/components/ui/sidebar';

describe('SidebarMenuSkeleton', () => {
    test('mantiene un ancho decorativo determinista entre renderizados SSR', () => {
        const first = renderToStaticMarkup(<SidebarMenuSkeleton />);
        const second = renderToStaticMarkup(<SidebarMenuSkeleton />);

        expect(first).toContain('--skeleton-width:70%');
        expect(second).toBe(first);
        expect(first).toContain('data-sidebar="menu-skeleton-text"');
    });

    test('conserva el icono opcional y los atributos del llamador', () => {
        const markup = renderToStaticMarkup(
            <SidebarMenuSkeleton showIcon data-cy="loading-navigation" />,
        );

        expect(markup).toContain('data-sidebar="menu-skeleton-icon"');
        expect(markup).toContain('data-cy="loading-navigation"');
    });
});
