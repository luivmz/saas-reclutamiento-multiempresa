import { useEffect, useRef, useState, type HTMLAttributes } from 'react';
import { REDUCED_MOTION_QUERY } from '@/components/experience-3d/use-scene-capability';
import { someIntersecting } from '@/lib/intersection';
import { cn } from '@/lib/utils';

export type RevealState = 'static' | 'hidden' | 'shown';

type RevealWindow = Pick<Window, 'matchMedia' | 'innerHeight'> & {
    IntersectionObserver?: typeof IntersectionObserver;
};

/**
 * Decide y vigila el estado de un bloque; devuelve su limpieza. Va aparte del
 * componente para poder probarlo sin navegador.
 *
 * - Lo que al montar ya se ve, o todo si hay movimiento reducido o no hay
 *   `IntersectionObserver`, se queda estático: no se oculta nunca.
 * - Lo de abajo se oculta y entra la primera vez que se ve, aunque el aviso
 *   inicial («fuera») y el siguiente («dentro») lleguen juntos (DEF-19).
 * - **Si el movimiento reducido se activa con la página abierta (VIS-L01)**,
 *   lo que seguía oculto pasa a estático en ese momento, sin desplazamiento.
 * - Cada bloque cambia de estado **una sola vez** después de ocultarse: al
 *   asentarse se desconecta el observador y se retira la escucha del
 *   movimiento reducido, así que nada posterior lo vuelve a ocultar.
 */
export function watchReveal(
    element: Element,
    win: RevealWindow,
    onState: (state: RevealState) => void,
): () => void {
    const Observer = win.IntersectionObserver;
    const motion = win.matchMedia(REDUCED_MOTION_QUERY);

    if (
        !Observer ||
        motion.matches ||
        element.getBoundingClientRect().top < win.innerHeight
    ) {
        return () => {};
    }

    let settled = false;
    // Todas las entradas del aviso, no solo la primera (DEF-19).
    const observer = new Observer(
        (entries) => {
            if (someIntersecting(entries)) {
                settle('shown');
            }
        },
        { rootMargin: '0px 0px -10% 0px' },
    );
    const onMotion = () => {
        if (motion.matches) {
            settle('static');
        }
    };
    const stop = () => {
        observer.disconnect();
        motion.removeEventListener('change', onMotion);
    };

    function settle(state: RevealState) {
        if (settled) {
            return;
        }

        settled = true;
        stop();
        onState(state);
    }

    onState('hidden');
    observer.observe(element);
    motion.addEventListener('change', onMotion);

    return stop;
}

/**
 * Entrada discreta al desplazarse, solo para secciones de la portada.
 *
 * Lo que garantiza:
 *
 * - **Sin JavaScript, o antes de montar, el contenido se ve**: el estado
 *   inicial es estático y visible. Solo se oculta lo que, al montar, está por
 *   debajo del borde de la ventana; lo que ya se ve nunca parpadea.
 * - **Con movimiento reducido no oculta nada**, tampoco si se activa con la
 *   página abierta: lo pendiente aparece en su sitio, sin desplazarse
 *   (`watchReveal`; además, `app.css` lo muestra aunque el script no llegue a
 *   reaccionar).
 * - **No toca la interacción**: es opacidad y un desplazamiento de 16 px por
 *   CSS (`[data-reveal]` en `app.css`); el contenido sigue en el DOM, con su
 *   orden de lectura y de tabulación.
 */
export function Reveal({
    className,
    delay = 0,
    style,
    ...props
}: HTMLAttributes<HTMLDivElement> & { delay?: number }) {
    const ref = useRef<HTMLDivElement>(null);
    const [state, setState] = useState<RevealState>('static');

    useEffect(() => {
        const element = ref.current;

        return element ? watchReveal(element, window, setState) : undefined;
    }, []);

    return (
        <div
            ref={ref}
            data-reveal={state}
            className={cn(className)}
            style={
                state === 'static'
                    ? style
                    : { ...style, transitionDelay: `${delay}ms` }
            }
            {...props}
        />
    );
}
