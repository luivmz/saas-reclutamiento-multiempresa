import { Form, Head } from '@inertiajs/react';
import InputError from '@/components/input-error';
import { ApplicationRequirements } from '@/components/jobs/application-requirements';
import { ReturnNotice } from '@/components/jobs/return-notice';
import PasswordInput from '@/components/password-input';
import TextLink from '@/components/text-link';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Spinner } from '@/components/ui/spinner';
import { login } from '@/routes';
import { store } from '@/routes/register';
import type {
    ApplicationRequirements as Requirements,
    ChosenVacancy,
} from '@/types';

type Props = {
    passwordRules: string;
    convocatoria: ChosenVacancy | null;
    requisitos: Requirements;
};

export default function Register({
    passwordRules,
    convocatoria,
    requisitos,
}: Props) {
    // Pasar al acceso conserva la convocatoria elegida.
    const query = convocatoria ? { convocatoria: convocatoria.id } : undefined;

    return (
        <>
            <Head title="Crear cuenta" />
            {convocatoria && (
                <ReturnNotice vacancy={convocatoria} context="register" />
            )}
            <Form
                {...store.form()}
                resetOnSuccess={['password', 'password_confirmation']}
                disableWhileProcessing
                className="flex flex-col gap-6"
            >
                {({ processing, errors }) => (
                    <>
                        <div className="grid gap-5">
                            <div className="grid gap-2">
                                <Label htmlFor="name">
                                    Nombres y apellidos
                                </Label>
                                <Input
                                    id="name"
                                    type="text"
                                    required
                                    autoFocus
                                    autoComplete="name"
                                    name="name"
                                    placeholder="Nombre completo"
                                    data-cy="register-name"
                                />
                                <InputError
                                    message={errors.name}
                                    className="mt-2"
                                />
                            </div>

                            <div className="grid gap-2">
                                <Label htmlFor="email">
                                    Correo electrónico
                                </Label>
                                <Input
                                    id="email"
                                    type="email"
                                    required
                                    autoComplete="email"
                                    name="email"
                                    placeholder="usuario@ejemplo.test"
                                    data-cy="register-email"
                                />
                                <InputError message={errors.email} />
                            </div>

                            <div className="grid gap-2">
                                <Label htmlFor="password">Contraseña</Label>
                                <PasswordInput
                                    id="password"
                                    required
                                    autoComplete="new-password"
                                    name="password"
                                    placeholder="Contraseña"
                                    passwordrules={passwordRules}
                                    data-cy="register-password"
                                />
                                <InputError message={errors.password} />
                            </div>

                            <div className="grid gap-2">
                                <Label htmlFor="password_confirmation">
                                    Confirmar contraseña
                                </Label>
                                <PasswordInput
                                    id="password_confirmation"
                                    required
                                    autoComplete="new-password"
                                    name="password_confirmation"
                                    placeholder="Repita la contraseña"
                                    passwordrules={passwordRules}
                                    data-cy="register-password-confirmation"
                                />
                                <InputError
                                    message={errors.password_confirmation}
                                />
                            </div>

                            <Button
                                type="submit"
                                className="w-full"
                                data-test="register-user-button"
                                data-cy="register-submit"
                            >
                                {processing && <Spinner />}
                                Crear cuenta de postulante
                            </Button>
                        </div>

                        <div className="bg-surface space-y-1.5 rounded-md border px-3 py-3">
                            <p className="text-sm font-medium">
                                Después de crear la cuenta
                            </p>
                            <ApplicationRequirements
                                requirements={requisitos}
                                compact
                            />
                        </div>

                        <p className="text-muted-foreground text-center text-sm">
                            ¿Ya tiene una cuenta?{' '}
                            <TextLink href={login({ query })}>
                                Inicie sesión
                            </TextLink>
                        </p>
                    </>
                )}
            </Form>
        </>
    );
}

Register.layout = {
    title: 'Cree su cuenta de postulante',
    description:
        'Con su cuenta podrá completar su perfil, cargar su CV y postular a las convocatorias vigentes.',
};
