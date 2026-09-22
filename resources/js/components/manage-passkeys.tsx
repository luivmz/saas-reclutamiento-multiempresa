import { router } from '@inertiajs/react';
import { KeyRound } from 'lucide-react';
import { destroy } from '@/actions/Laravel/Passkeys/Http/Controllers/PasskeyRegistrationController';
import { Section } from '@/components/page';
import PasskeyItem from '@/components/passkey-item';
import PasskeyRegistration from '@/components/passkey-register';
import type { Passkey } from '@/types/auth';

export type Props = {
    canManagePasskeys?: boolean;
    passkeys?: Passkey[];
};

const NoPasskeys = () => {
    return (
        <div className="p-8 text-center">
            <div className="bg-surface mx-auto mb-4 flex size-12 items-center justify-center rounded-full">
                <KeyRound
                    className="text-muted-foreground size-5"
                    aria-hidden="true"
                />
            </div>
            <p className="font-medium">Todavía no tiene claves de acceso</p>
            <p className="text-muted-foreground mx-auto mt-1 max-w-sm text-sm leading-relaxed">
                Registre una para entrar con la huella, el rostro o el PIN de su
                dispositivo, sin escribir la contraseña.
            </p>
        </div>
    );
};

export default function ManagePasskeys(props: Props) {
    const passkeys = props.passkeys ?? [];

    const handleDelete = (id: number, onError: () => void) => {
        router.delete(destroy.url(id), {
            preserveScroll: true,
            onError,
        });
    };

    const handleRegisterSuccess = () => {
        router.reload();
    };

    if (!(props.canManagePasskeys ?? false)) {
        return null;
    }

    return (
        <Section
            title="Claves de acceso"
            description="Entre sin contraseña usando la huella, el rostro o el PIN de su dispositivo."
        >
            <div className="space-y-5">
                <div className="overflow-hidden rounded-lg border">
                    {passkeys.length > 0 ? (
                        passkeys.map((passkey) => (
                            <PasskeyItem
                                key={passkey.id}
                                passkey={passkey}
                                onDelete={handleDelete}
                            />
                        ))
                    ) : (
                        <NoPasskeys />
                    )}
                </div>

                <PasskeyRegistration onSuccess={handleRegisterSuccess} />
            </div>
        </Section>
    );
}
