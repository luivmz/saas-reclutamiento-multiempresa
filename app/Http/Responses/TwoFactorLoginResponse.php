<?php

namespace App\Http\Responses;

use App\Http\Support\ConvocatoriaDeRetorno;
use Laravel\Fortify\Http\Responses\TwoFactorLoginResponse as Base;

/**
 * Respuesta tras el acceso con segundo factor: si un postulante venía de una convocatoria, vuelve a ella (ConvocatoriaDeRetorno).
 * El resto lo decide la respuesta original, que ya redirige a la URL «intended».
 *
 * La respuesta JSON de Fortify no consume esa URL: fijarla dejaría un destino pendiente en la sesión que otra
 * redirección posterior (por ejemplo, confirmar la contraseña) usaría. Por eso solo se prepara al redirigir.
 */
class TwoFactorLoginResponse extends Base
{
    public function toResponse($request)
    {
        if (! $request->wantsJson()) {
            app(ConvocatoriaDeRetorno::class)->prepararDestino($request);
        }

        return parent::toResponse($request);
    }
}
