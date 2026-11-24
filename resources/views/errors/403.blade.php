@extends('errors::marca')

@php
    try {
        $conSesion = auth()->check();
    } catch (\Throwable) {
        $conSesion = false;
    }
@endphp

@section('title', 'Acceso no permitido')
@section('code', '403')
@section('heading', 'No tiene permiso para ver esta página')
{{-- Nunca se imprime el mensaje de la excepción: puede describir reglas internas de autorización. --}}
@section('message', 'Su cuenta no tiene acceso a esta sección. Si cree que debería tenerlo, consulte con la persona que administra su organización.')

@section('actions')
    @if ($conSesion)
        <a class="boton primario" href="/dashboard">Ir a mi panel</a>
    @else
        <a class="boton primario" href="/login">Iniciar sesión</a>
    @endif
    <a class="boton" href="/empleos">Ver empleos disponibles</a>
@endsection
