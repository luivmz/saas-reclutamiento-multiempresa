{{--
    Plantilla de las páginas de error (DEF-28).

    Es HTML autónomo: estilos en línea, marca en SVG en línea y fuentes del sistema. No usa Vite, la base de datos,
    la caché ni la sesión, así que también se muestra cuando esos servicios fallan (la página 500 depende de eso).
    El tema sigue la cookie `appearance` (no cifrada) o, si no existe, la preferencia del sistema.
--}}
@php
    try {
        $tema = request()->cookie('appearance');
    } catch (\Throwable) {
        $tema = null;
    }
    $tema = in_array($tema, ['light', 'dark'], true) ? $tema : null;
@endphp
<!DOCTYPE html>
<html lang="es" @if ($tema) class="{{ $tema }}" @endif>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="noindex">
    <title>@yield('title') - {{ config('app.name', 'SaaS Reclutamiento') }}</title>
    <link rel="icon" href="/favicon.ico" sizes="any">
    <link rel="icon" href="/favicon.svg" type="image/svg+xml">
    <style>
        :root {
            --fondo: #f5f9fa; --texto: #162027; --tenue: #4a5961; --tarjeta: #ffffff; --borde: #d5dee2;
            --primario: #07616f; --sobre-primario: #ffffff; color-scheme: light;
        }
        @media (prefers-color-scheme: dark) {
            :root:not(.light) {
                --fondo: #0d161a; --texto: #e7eef0; --tenue: #9fb0b7; --tarjeta: #141f24; --borde: #273840;
                --primario: #63b8bd; --sobre-primario: #0d161a; color-scheme: dark;
            }
        }
        :root.dark {
            --fondo: #0d161a; --texto: #e7eef0; --tenue: #9fb0b7; --tarjeta: #141f24; --borde: #273840;
            --primario: #63b8bd; --sobre-primario: #0d161a; color-scheme: dark;
        }
        * { box-sizing: border-box; }
        html, body { margin: 0; }
        body {
            min-height: 100vh; background: var(--fondo); color: var(--texto);
            font: 16px/1.6 'IBM Plex Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;
            display: flex; align-items: center; justify-content: center; padding: 32px 16px;
        }
        main { width: 100%; max-width: 34rem; }
        .marca {
            display: inline-flex; align-items: center; gap: 10px; margin-bottom: 20px; color: var(--texto);
            text-decoration: none; font: 600 16px/1.2 'IBM Plex Serif', Georgia, serif;
        }
        .baldosa {
            display: inline-flex; width: 36px; height: 36px; border-radius: 8px; align-items: center;
            justify-content: center; background: var(--primario); color: var(--sobre-primario);
        }
        .tarjeta { background: var(--tarjeta); border: 1px solid var(--borde); border-radius: 14px; padding: 28px 24px; }
        .codigo { margin: 0 0 6px; color: var(--tenue); font-size: 14px; }
        h1 { margin: 0 0 10px; font: 600 clamp(24px, 6vw, 30px)/1.2 'IBM Plex Serif', Georgia, serif; }
        .mensaje { margin: 0 0 22px; color: var(--tenue); }
        .acciones { display: flex; flex-wrap: wrap; gap: 10px; }
        .boton {
            display: inline-flex; align-items: center; justify-content: center; min-height: 44px; padding: 10px 16px;
            border-radius: 8px; border: 1px solid var(--borde); color: var(--texto); background: transparent;
            font-weight: 600; font-size: 15px; text-decoration: none;
        }
        .boton.primario { background: var(--primario); border-color: var(--primario); color: var(--sobre-primario); }
        .boton:hover { text-decoration: underline; text-underline-offset: 3px; }
        a:focus-visible { outline: 3px solid var(--primario); outline-offset: 3px; }
        @media (max-width: 420px) { .boton { flex: 1 1 100%; } .tarjeta { padding: 24px 18px; } }
    </style>
</head>
<body>
    <main>
        <a class="marca" href="/">
            <span class="baldosa" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" focusable="false">
                    <rect x="2" y="4" width="15" height="3" rx="1.5"/><rect x="2" y="10" width="10" height="3" rx="1.5"/>
                    <rect x="2" y="16" width="13" height="3" rx="1.5"/><circle cx="20" cy="11.5" r="2.5"/>
                </svg>
            </span>
            {{ config('app.name', 'SaaS Reclutamiento') }}
        </a>
        <section class="tarjeta" aria-labelledby="titulo-error">
            <p class="codigo">Error @yield('code')</p>
            <h1 id="titulo-error">@yield('heading')</h1>
            <p class="mensaje">@yield('message')</p>
            <nav class="acciones" aria-label="Cómo continuar">
                @yield('actions')
            </nav>
        </section>
    </main>
</body>
</html>
