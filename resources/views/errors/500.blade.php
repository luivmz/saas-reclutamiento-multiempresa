@extends('errors::marca')

@php
    // Sin sesión ni base de datos: esta página debe mostrarse aunque fallen. Reintentar repite solo una lectura (GET)
    // y siempre dentro de esta aplicación.
    $ruta = trim(request()->path(), '/');
    $reintentar = request()->isMethod('GET') && $ruta !== '' ? '/'.$ruta : '/';
@endphp

@section('title', 'Error del servidor')
@section('code', '500')
@section('heading', 'Algo falló de nuestro lado')
@section('message', 'No pudimos completar la solicitud. No es un problema de su cuenta ni de lo que ingresó. Inténtelo de nuevo en unos minutos.')

@section('actions')
    <a class="boton primario" href="{{ $reintentar }}">Reintentar</a>
    <a class="boton" href="/">Ir al inicio</a>
@endsection
