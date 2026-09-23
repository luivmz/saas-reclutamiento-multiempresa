import {
    Component,
    lazy,
    Suspense,
    useEffect,
    useRef,
    useState,
    type ReactNode,
} from 'react';
import { RecruitmentScenePoster } from './recruitment-scene-poster';
import { useSceneCapability } from './use-scene-capability';

/**
 * Capa de profundidad detrás del expediente de la portada (ADR-003).
 *
 * Lo que esta capa garantiza, en este orden:
 *
 * 1. **El póster se ve al instante** y ocupa exactamente la caja de la
 *    tarjeta: la capa es absoluta, así que cambiar póster por escena no mueve
 *    nada de la página.
 * 2. **La escena se descarga solo si procede y solo al entrar en el
 *    viewport.** Vive en su propio fragmento: quien usa móvil, movimiento
 *    reducido, ahorro de datos o un equipo modesto no descarga ni un byte de
 *    ella.
 * 3. **Si la escena falla —el fragmento no llega o revienta al montar— queda
 *    el póster**, y la página sigue completa.
 * 4. **Es decorativa de principio a fin**: `aria-hidden`, `inert`, sin
 *    eventos de puntero. Todo lo que dice la portada está en el DOM de al
 *    lado.
 */
const RecruitmentScene = lazy(() => import('./recruitment-scene'));

class SceneBoundary extends Component<
    { fallback: ReactNode; children: ReactNode },
    { failed: boolean }
> {
    state = { failed: false };

    static getDerivedStateFromError() {
        return { failed: true };
    }

    render() {
        return this.state.failed ? this.props.fallback : this.props.children;
    }
}

/** Pasa a `true` la primera vez que el elemento entra en el viewport, y ahí se queda. */
function useSeenOnce<T extends Element>(ref: React.RefObject<T | null>) {
    const [seen, setSeen] = useState(false);

    useEffect(() => {
        const element = ref.current;

        if (!element || seen) {
            return;
        }

        const observer = new IntersectionObserver(([entry]) => {
            if (entry.isIntersecting) {
                setSeen(true);
                observer.disconnect();
            }
        });

        observer.observe(element);

        return () => observer.disconnect();
    }, [ref, seen]);

    return seen;
}

export function RecruitmentDepth() {
    const ref = useRef<HTMLDivElement>(null);
    const { mode, reason } = useSceneCapability();
    const seen = useSeenOnce(ref);
    const showScene = mode === 'scene' && seen;
    const poster = <RecruitmentScenePoster />;

    return (
        <div
            ref={ref}
            aria-hidden="true"
            inert
            className="pointer-events-none absolute inset-0 select-none"
            data-cy="recruitment-depth"
            data-mode={mode}
            data-reason={reason}
        >
            {showScene ? (
                <SceneBoundary fallback={poster}>
                    <Suspense fallback={poster}>
                        <RecruitmentScene />
                    </Suspense>
                </SceneBoundary>
            ) : (
                poster
            )}
        </div>
    );
}
