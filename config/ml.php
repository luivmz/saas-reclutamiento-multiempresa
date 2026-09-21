<?php

/*
| Servicio de riesgo operacional (Fase 15C) consumido desde Laravel (Fase 16).
|
| El servicio es EXPERIMENTAL: estima la probabilidad de retraso de un proceso
| de vacante y nunca evalúa, puntúa ni ordena personas. Su resultado es una
| señal para revisión humana; la decisión final sigue siendo humana (RF-23).
|
| El servicio NO debe exponerse fuera de la red interna.
*/

return [

    /*
    | Interruptor general. Con `false` Laravel ni siquiera intenta la llamada y
    | todo el sistema cae al panel descriptivo. Es el modo por omisión: la
    | integración se activa a conciencia, no por defecto.
    */
    'enabled' => filter_var(env('ML_SERVICE_ENABLED', false), FILTER_VALIDATE_BOOL),

    /*
    | Base del servicio. En desarrollo con Docker, Laravel corre en un
    | contenedor y el servicio en el host, así que la URL suele ser
    | `http://host.docker.internal:8008`. Fuera de Docker, `127.0.0.1:8008`.
    |
    | 8008 y no 8001: ese puerto ya lo ocupa `app-e2e` (`E2E_APP_PORT`).
    */
    'base_url' => rtrim((string) env('ML_SERVICE_URL', 'http://127.0.0.1:8008'), '/'),

    /*
    | Tiempos de espera, en segundos. Cortos a propósito: una estimación de
    | riesgo es información auxiliar y jamás debe hacer esperar al usuario en
    | el flujo principal de reclutamiento.
    */
    'connect_timeout' => (float) env('ML_SERVICE_CONNECT_TIMEOUT', 1.0),
    'timeout' => (float) env('ML_SERVICE_TIMEOUT', 3.0),

    /*
    | Reintentos ante fallos transitorios. Uno como máximo: el servicio es de
    | una sola instancia y reintentar en bucle solo añade latencia al usuario y
    | carga a un servicio que ya está sufriendo.
    */
    'retries' => (int) env('ML_SERVICE_RETRIES', 1),
    'retry_delay_ms' => (int) env('ML_SERVICE_RETRY_DELAY_MS', 150),

    /*
    | Token compartido de servicio a servicio. Vive SOLO en el entorno, nunca
    | en el repositorio, y no se registra en los logs. Vacío significa sin
    | autenticación, admisible únicamente en desarrollo local.
    */
    'internal_token' => env('ML_SERVICE_TOKEN'),

    /*
    | Identidad del experimento aprobado en la Fase 15B. Si el servicio
    | responde con otra huella u otro umbral, la respuesta se descarta: estaría
    | sirviendo un modelo distinto del que el equipo auditó.
    */
    'expected_freeze_fingerprint' => env(
        'ML_EXPECTED_FREEZE_FINGERPRINT',
        '9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2'
    ),
    'expected_threshold' => (float) env('ML_EXPECTED_THRESHOLD', 0.1679418172266036),

];
