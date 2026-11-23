/**
 * Lectura de los avisos de IntersectionObserver (DEF-19).
 *
 * Un aviso trae, en orden, todas las entradas acumuladas desde el anterior.
 * Si la página se desplaza justo después de empezar a observar —una recarga
 * que restaura el desplazamiento, o alguien que baja de inmediato—, el aviso
 * inicial («fuera de la vista») y el siguiente («dentro») pueden llegar en el
 * mismo lote. Quien lee solo la primera entrada se queda con «fuera» y, como
 * el estado ya no vuelve a cambiar, no recibe otro aviso: el bloque queda
 * oculto para siempre.
 */
type Entry = Pick<IntersectionObserverEntry, 'isIntersecting'>;

/** Para «la primera vez que se ve»: si alguna entrada del lote estuvo a la vista. */
export function someIntersecting(entries: readonly Entry[]): boolean {
    return entries.some((entry) => entry.isIntersecting);
}

/** Para «¿se ve ahora?»: el estado de la última entrada, o `null` si no hay ninguna. */
export function latestIntersecting(entries: readonly Entry[]): boolean | null {
    return entries.length ? entries[entries.length - 1].isIntersecting : null;
}
