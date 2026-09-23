/**
 * Salto al contenido.
 *
 * La barra lateral tiene hasta diez enlaces: sin este atajo, quien navega con
 * teclado los recorría todos en cada página antes de llegar a la tabla. El
 * enlace está siempre en el DOM y solo se ve al recibir el foco.
 */
export const MAIN_CONTENT_ID = 'contenido-principal';

export function SkipLink() {
    return (
        <a
            href={`#${MAIN_CONTENT_ID}`}
            className="bg-primary text-primary-foreground sr-only rounded-md text-sm font-medium focus:not-sr-only focus:fixed focus:top-3 focus:left-3 focus:z-50 focus:px-4 focus:py-2"
        >
            Saltar al contenido
        </a>
    );
}
