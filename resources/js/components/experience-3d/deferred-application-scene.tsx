import { useEffect, useRef, useState } from 'react';
import { latestIntersecting } from '@/lib/intersection';
import {
    startApplicationScene,
    type ApplicationStep,
    type LoadApplicationScene,
    type SceneStatus,
} from './application-scene-session';
import { useSceneCapability } from './use-scene-capability';

export default function DeferredApplicationScene({
    step,
    load,
    onStepChange,
}: {
    step: ApplicationStep;
    load: LoadApplicationScene;
    onStepChange: (step: ApplicationStep) => void;
}) {
    const { mode } = useSceneCapability();
    const [failed, setFailed] = useState(false);

    if (mode !== 'scene' || failed) {
        return null;
    }

    return (
        <ObservedScene
            step={step}
            load={load}
            onStepChange={onStepChange}
            onFailure={setFailed}
        />
    );
}

function ObservedScene({
    step,
    load,
    onFailure,
    onStepChange,
}: {
    step: ApplicationStep;
    load: LoadApplicationScene;
    onFailure: (failed: boolean) => void;
    onStepChange: (step: ApplicationStep) => void;
}) {
    const surface = useRef<HTMLDivElement>(null);
    const [near, setNear] = useState(false);
    const [playing, setPlaying] = useState(false);

    useEffect(() => {
        const element = surface.current;
        if (!element || !window.IntersectionObserver) {
            return;
        }

        let visible = false;
        const updatePlayback = () => setPlaying(visible && !document.hidden);

        const proximity = new IntersectionObserver(
            (entries) => {
                setNear(latestIntersecting(entries) === true);
            },
            { rootMargin: '120px 0px' },
        );
        const visibility = new IntersectionObserver((entries) => {
            visible = latestIntersecting(entries) === true;
            updatePlayback();
        });
        proximity.observe(element);
        visibility.observe(element);
        document.addEventListener('visibilitychange', updatePlayback);

        return () => {
            proximity.disconnect();
            visibility.disconnect();
            document.removeEventListener('visibilitychange', updatePlayback);
        };
    }, []);

    return (
        <div ref={surface} className="absolute inset-0">
            {near && (
                <SceneCanvas
                    step={step}
                    load={load}
                    playing={playing}
                    onStepChange={onStepChange}
                    onFailure={onFailure}
                />
            )}
        </div>
    );
}

function SceneCanvas({
    step,
    load,
    playing,
    onFailure,
    onStepChange,
}: {
    step: ApplicationStep;
    load: LoadApplicationScene;
    playing: boolean;
    onStepChange: (step: ApplicationStep) => void;
    onFailure: (failed: boolean) => void;
}) {
    const canvas = useRef<HTMLCanvasElement>(null);
    const instance = useRef<ReturnType<typeof startApplicationScene>>(null);
    const [status, setStatus] = useState<SceneStatus>('loading');

    useEffect(() => {
        const element = canvas.current;
        if (!element) {
            return;
        }

        const room = startApplicationScene(
            element,
            load,
            (next) => {
                setStatus(next);
                if (next === 'error') {
                    onFailure(true);
                }
            },
            onStepChange,
        );
        instance.current = room;
        return () => {
            room.dispose();
            instance.current = null;
        };
    }, [load, onFailure, onStepChange]);

    useEffect(() => {
        instance.current?.setStep(step);
    }, [step, load]);

    useEffect(() => {
        instance.current?.setPlaying(playing);
    }, [playing, load]);

    return (
        <canvas
            ref={canvas}
            tabIndex={-1}
            data-status={status}
            className="absolute inset-0 size-full touch-pan-y data-[status=error]:opacity-0 data-[status=loading]:opacity-0 data-[status=ready]:pointer-events-auto"
        />
    );
}
