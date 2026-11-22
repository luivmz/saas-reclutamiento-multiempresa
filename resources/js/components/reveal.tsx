import { useEffect, useRef, useState, type HTMLAttributes } from 'react';
import { REDUCED_MOTION_QUERY } from '@/components/experience-3d/use-scene-capability';
import { cn } from '@/lib/utils';

type RevealState = 'static' | 'hidden' | 'shown';

/**
 * Entrada discreta al desplazarse, solo para secciones de la portada.
 *
 * Lo que garantiza:
 *
 * - **Sin JavaScript, o antes de montar, el contenido se ve**: el estado
 *   inicial es estático y visible. Solo se oculta lo que, al montar, está por
 *   debajo del borde de la ventana; lo que ya se ve nunca parpadea.
 * - **Con movimiento reducido no hace nada**: ni se oculta ni se desplaza.
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

        if (
            !element ||
            typeof IntersectionObserver === 'undefined' ||
            window.matchMedia(REDUCED_MOTION_QUERY).matches ||
            element.getBoundingClientRect().top < window.innerHeight
        ) {
            return;
        }

        setState('hidden');
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (entry.isIntersecting) {
                    setState('shown');
                    observer.disconnect();
                }
            },
            { rootMargin: '0px 0px -10% 0px' },
        );

        observer.observe(element);

        return () => observer.disconnect();
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
