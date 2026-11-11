<?php

/*
 * Capacidades experimentales de la rama local `exp/evidencias-ml02`.
 *
 * Están DESACTIVADAS por defecto. Solo el entorno experimental (proyecto Docker `experimental`) las activa
 * con EXPERIMENTAL_EVIDENCIAS=true. No constituyen la integración formal en el SaaS: esa integración sigue
 * condicionada a la G0 real, un ADR de alcance y la decisión N5 (EI-23). F37-SBX sigue BLOQUEADA.
 */
return [
    // Flujo de evidencias ficticias por postulación (registrar, consultar, versionar) y la ayuda documental
    // ML-02 (recuperación léxica de fragmentos por criterio, con fuentes). Sin puntajes sobre personas.
    'evidencias' => (bool) env('EXPERIMENTAL_EVIDENCIAS', false),
];
