<?php

namespace App\Http\Responses;

use App\Http\Support\ConvocatoriaDeRetorno;
use Laravel\Fortify\Http\Responses\TwoFactorLoginResponse as Base;

/**
 * Respuesta tras el acceso con segundo factor: si un postulante venía de una convocatoria, vuelve a ella (ConvocatoriaDeRetorno).
 * El resto lo decide la respuesta original, que ya redirige a la URL «intended».
 */
class TwoFactorLoginResponse extends Base
{
    public function toResponse($request)
    {
        app(ConvocatoriaDeRetorno::class)->prepararDestino($request);

        return parent::toResponse($request);
    }
}
