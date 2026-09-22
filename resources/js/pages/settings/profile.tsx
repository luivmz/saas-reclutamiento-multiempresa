import { Form, Head, usePage } from '@inertiajs/react';
import ProfileController from '@/actions/App/Http/Controllers/Settings/ProfileController';
import DeleteUser from '@/components/delete-user';
import { FormField } from '@/components/form-controls';
import { Section } from '@/components/page';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Spinner } from '@/components/ui/spinner';
import { edit } from '@/routes/profile';
import type { Auth } from '@/types';

type PageProps = {
    auth: Auth;
};

export default function Profile() {
    const { auth } = usePage<PageProps>().props;

    return (
        <>
            <Head title="Perfil de la cuenta" />

            <Section
                title="Perfil"
                description="Su nombre y su correo de acceso."
            >
                <Form
                    {...ProfileController.update.form()}
                    options={{ preserveScroll: true }}
                    className="max-w-lg space-y-5"
                >
                    {({ processing, errors }) => (
                        <>
                            <FormField
                                label="Nombre"
                                htmlFor="name"
                                error={errors.name}
                                required
                            >
                                <Input
                                    id="name"
                                    name="name"
                                    defaultValue={auth.user.name}
                                    required
                                    autoComplete="name"
                                    placeholder="Nombre y apellidos"
                                />
                            </FormField>

                            <FormField
                                label="Correo electrónico"
                                htmlFor="email"
                                error={errors.email}
                                required
                            >
                                <Input
                                    id="email"
                                    type="email"
                                    name="email"
                                    defaultValue={auth.user.email}
                                    required
                                    autoComplete="username"
                                    placeholder="usuario@ejemplo.test"
                                />
                            </FormField>

                            <Button
                                disabled={processing}
                                data-test="update-profile-button"
                            >
                                {processing && <Spinner />}
                                Guardar cambios
                            </Button>
                        </>
                    )}
                </Form>
            </Section>

            <DeleteUser />
        </>
    );
}

Profile.layout = {
    breadcrumbs: [{ title: 'Perfil de la cuenta', href: edit() }],
};
