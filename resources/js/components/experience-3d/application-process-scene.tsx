import { Component, lazy, Suspense, type ReactNode } from 'react';
import type {
    ApplicationStep,
    LoadApplicationScene,
} from './application-scene-session';
import { useSceneCapability } from './use-scene-capability';

const DeferredApplicationScene = lazy(
    () => import('./deferred-application-scene'),
);

class SceneBoundary extends Component<
    { children: ReactNode },
    { failed: boolean }
> {
    state = { failed: false };

    static getDerivedStateFromError() {
        return { failed: true };
    }

    render() {
        return this.state.failed ? null : this.props.children;
    }
}

export function ApplicationProcessScene({
    step,
    poster,
    load,
    onStepChange,
}: {
    step: ApplicationStep;
    poster: ReactNode;
    load?: LoadApplicationScene;
    onStepChange: (step: ApplicationStep) => void;
}) {
    // El fragmento diferido solo se pide y se monta si la escena procede: en
    // móvil, con movimiento reducido o en equipos modestos queda el póster sin
    // descargar ni montar nada.
    const { mode } = useSceneCapability();

    return (
        <div
            aria-hidden="true"
            className="group bg-surface pointer-events-none relative min-w-0 overflow-hidden rounded-xl border"
            data-cy="apply-illustration"
        >
            <div className="group-has-[canvas[data-status=ready]]:invisible">
                {poster}
            </div>
            {load && mode === 'scene' && (
                <SceneBoundary>
                    <Suspense fallback={null}>
                        <DeferredApplicationScene
                            step={step}
                            load={load}
                            onStepChange={onStepChange}
                        />
                    </Suspense>
                </SceneBoundary>
            )}
        </div>
    );
}
