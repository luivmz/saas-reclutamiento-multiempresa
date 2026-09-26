/**
 * Comportamiento de desplazamiento según la preferencia de movimiento.
 *
 * La política global de la Fase 19 fija `scroll-behavior: auto` con
 * movimiento reducido, pero eso solo gobierna el desplazamiento que decide el
 * CSS. Un `scrollIntoView({ behavior: 'smooth' })` lo pide explícitamente y
 * pasa por encima de esa regla, así que el código que desplaza tiene que
 * preguntar por la preferencia él mismo.
 */
export function preferredScrollBehavior(
    win: Pick<Window, 'matchMedia'> | undefined = typeof window === 'undefined'
        ? undefined
        : window,
): ScrollBehavior {
    if (!win) {
        return 'auto';
    }

    return win.matchMedia('(prefers-reduced-motion: reduce)').matches
        ? 'auto'
        : 'smooth';
}
