import { Form } from '@inertiajs/react';
import { useRef } from 'react';
import ProfileController from '@/actions/App/Http/Controllers/Settings/ProfileController';
import InputError from '@/components/input-error';
import { Section } from '@/components/page';
import PasswordInput from '@/components/password-input';
import { Button } from '@/components/ui/button';
import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogTitle,
    DialogTrigger,
} from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';

/**
 * Eliminación de la cuenta.
 *
 * La advertencia dice exactamente qué se pierde y que no se puede deshacer, y
 * la confirmación pide la contraseña: es la acción más destructiva de toda la
 * aplicación y no debe poder ejecutarse por inercia.
 */
export default function DeleteUser() {
    const passwordInput = useRef<HTMLInputElement>(null);

    return (
        <Section
            title="Eliminar la cuenta"
            description="Se borran su cuenta y todos sus datos asociados."
            className="border-tone-danger-edge"
        >
            <div className="bg-tone-danger text-tone-danger-foreground ring-tone-danger-edge space-y-4 rounded-lg p-4 ring-1 ring-inset">
                <div className="space-y-1">
                    <p className="font-medium">
                        Esta acción no se puede deshacer
                    </p>
                    <p className="text-sm leading-relaxed">
                        Al eliminar la cuenta se borran de forma permanente sus
                        datos y su acceso a la plataforma.
                    </p>
                </div>

                <Dialog>
                    <DialogTrigger asChild>
                        <Button
                            variant="destructive"
                            data-test="delete-user-button"
                        >
                            Eliminar mi cuenta
                        </Button>
                    </DialogTrigger>
                    <DialogContent>
                        <DialogTitle>
                            ¿Confirma que desea eliminar su cuenta?
                        </DialogTitle>
                        <DialogDescription>
                            Se eliminarán de forma permanente su cuenta y todos
                            sus datos. Escriba su contraseña para confirmar.
                        </DialogDescription>

                        <Form
                            {...ProfileController.destroy.form()}
                            options={{ preserveScroll: true }}
                            onError={() => passwordInput.current?.focus()}
                            resetOnSuccess
                            className="space-y-6"
                        >
                            {({ resetAndClearErrors, processing, errors }) => (
                                <>
                                    <div className="grid gap-2">
                                        <Label
                                            htmlFor="password"
                                            className="sr-only"
                                        >
                                            Contraseña
                                        </Label>

                                        <PasswordInput
                                            id="password"
                                            name="password"
                                            ref={passwordInput}
                                            placeholder="Contraseña"
                                            autoComplete="current-password"
                                        />

                                        <InputError message={errors.password} />
                                    </div>

                                    <DialogFooter className="gap-2">
                                        <DialogClose asChild>
                                            <Button
                                                variant="secondary"
                                                onClick={() =>
                                                    resetAndClearErrors()
                                                }
                                            >
                                                Cancelar
                                            </Button>
                                        </DialogClose>

                                        <Button
                                            variant="destructive"
                                            disabled={processing}
                                            asChild
                                        >
                                            <button
                                                type="submit"
                                                data-test="confirm-delete-user-button"
                                            >
                                                Eliminar mi cuenta
                                            </button>
                                        </Button>
                                    </DialogFooter>
                                </>
                            )}
                        </Form>
                    </DialogContent>
                </Dialog>
            </div>
        </Section>
    );
}
