import { useSyncExternalStore } from 'react';

// Keep in sync with the sidebar's Tailwind lg breakpoint.
const DRAWER_QUERY = '(width < 64rem)';

const mql =
    typeof window === 'undefined' ? undefined : window.matchMedia(DRAWER_QUERY);

function mediaQueryListener(callback: (event: MediaQueryListEvent) => void) {
    if (!mql) {
        return () => {};
    }

    mql.addEventListener('change', callback);

    return () => {
        mql.removeEventListener('change', callback);
    };
}

function isSmallerThanBreakpoint(): boolean {
    return mql?.matches ?? false;
}

function getServerSnapshot(): boolean {
    return false;
}

export function useIsMobile(): boolean {
    return useSyncExternalStore(
        mediaQueryListener,
        isSmallerThanBreakpoint,
        getServerSnapshot,
    );
}
