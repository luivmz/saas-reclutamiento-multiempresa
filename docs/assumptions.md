# Supuestos y decisiones documentadas

Contexto: durante la Fase 0 **no se encontraron** F4, F5 (BPMN TO-BE), F6, casos de uso ni plan de pruebas en el equipo. Solo se hallaron 4 diagramas UML de PowerDesigner (despliegue y 3 de secuencia). La línea base funcional son los 27 RF entregados en el enunciado. Cada regla no derivable de esas fuentes se registra aquí con la opción más conservadora.

| ID | Tema | Supuesto / decisión | Motivo | Fuente relacionada |
|---|---|---|---|---|
| A-01 | Verificación de correo | Se desactiva `Features::emailVerification()` de Fortify. | Los usuarios demo usan correos ficticios; ningún RF exige verificación de correo. | RF-08 |
| A-02 | Herramientas | PHP 8.4 y Node 22 se ejecutan en Docker; no se usa el PHP 8.2 de XAMPP. | Laravel 13 exige PHP ≥ 8.3. | Enunciado §7 |
| A-03 | Pruebas backend | PHPUnit usa una base PostgreSQL dedicada (`reclutamiento_testing`), no SQLite. | Validar constraints e índices reales del motor de producción. | Enunciado §6 |
