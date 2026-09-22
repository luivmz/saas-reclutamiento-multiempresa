// Components
import { Form, Head } from '@inertiajs/react';
import { LoaderCircle } from 'lucide-react';
import InputError from '@/components/input-error';
import TextLink from '@/components/text-link';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { login } from '@/routes';
import { email } from '@/routes/password';

export default function ForgotPassword({ status }: { status?: string }) {
    return (
        <>
            <Head title="Recuperar la contraseña" />

            {status && (
                <p
                    role="status"
                    className="bg-tone-success text-tone-success-foreground ring-tone-success-edge rounded-md px-3 py-2 text-sm ring-1 ring-inset"
                >
                    {status}
                </p>
            )}

            <div className="space-y-6">
                <Form {...email.form()}>
                    {({ processing, errors }) => (
                        <>
                            <div className="grid gap-2">
                                <Label htmlFor="email">
                                    Correo electrónico
                                </Label>
                                <Input
                                    id="email"
                                    type="email"
                                    name="email"
                                    autoComplete="off"
                                    autoFocus
                                    placeholder="usuario@ejemplo.test"
                                />

                                <InputError message={errors.email} />
                            </div>

                            <div className="my-6 flex items-center justify-start">
                                <Button
                                    className="w-full"
                                    disabled={processing}
                                    data-test="email-password-reset-link-button"
                                >
                                    {processing && (
                                        <LoaderCircle
                                            className="size-4 animate-spin"
                                            aria-hidden="true"
                                        />
                                    )}
                                    Enviarme el enlace
                                </Button>
                            </div>
                        </>
                    )}
                </Form>

                <p className="text-muted-foreground text-center text-sm">
                    ¿Ya la recordó?{' '}
                    <TextLink href={login()}>Vuelva a iniciar sesión</TextLink>
                </p>
            </div>
        </>
    );
}

ForgotPassword.layout = {
    title: 'Recuperar la contraseña',
    description:
        'Escriba su correo y le enviaremos un enlace para restablecerla.',
};
