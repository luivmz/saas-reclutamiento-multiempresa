@extends('errors::marca')

@php
    try {
        $conSesion = auth()->check();
    } catch (\Throwable) {
        $conSesion = false;
    }
@endphp

@section('title', 'Página no encontrada')
@section('code', '404')
@section('heading', 'No encontramos esta página')
{{-- El mismo texto para lo que no existe y para lo que no está disponible para esta cuenta: no confirma nada de otras organizaciones. --}}
@section('message', 'La dirección no existe o su contenido no está disponible para esta cuenta. Revise el enlace o continúe desde aquí.')

@section('actions')
    @if ($conSesion)
        <a class="boton primario" href="/dashboard">Ir a mi panel</a>
        <a class="boton" href="/empleos">Ver empleos disponibles</a>
    @else
        <a class="boton primario" href="/empleos">Ver empleos disponibles</a>
        <a class="boton" href="/login">Iniciar sesión</a>
    @endif
@endsection
