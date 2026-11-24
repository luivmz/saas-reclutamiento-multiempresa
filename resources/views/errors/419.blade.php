@extends('errors::marca')

@php
    try {
        $conSesion = auth()->check();
    } catch (\Throwable) {
        $conSesion = false;
    }

    // Volver solo a una página de esta misma aplicación: se descarta cualquier otro origen y se usa una ruta relativa.
    $volver = '/';
    try {
        $origen = parse_url((string) request()->headers->get('referer'));
        if (is_array($origen) && ($origen['host'] ?? null) === request()->getHost() && in_array($origen['scheme'] ?? '', ['http', 'https'], true)) {
            $volver = '/'.ltrim($origen['path'] ?? '', '/').(isset($origen['query']) ? '?'.$origen['query'] : '');
        }
    } catch (\Throwable) {
        $volver = '/';
    }
@endphp

@section('title', 'La página expiró')
@section('code', '419')
@section('heading', 'La página expiró')
@section('message', 'Por seguridad, el formulario dejó de ser válido antes de enviarse y no se guardó nada. Vuelva a la página, recárguela e inténtelo de nuevo.')

@section('actions')
    <a class="boton primario" href="{{ $volver }}">Volver a la página</a>
    @if ($conSesion)
        <a class="boton" href="/dashboard">Ir a mi panel</a>
    @else
        <a class="boton" href="/login">Iniciar sesión</a>
    @endif
@endsection
