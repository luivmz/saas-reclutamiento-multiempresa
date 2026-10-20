# Prompts para las mejoras posteriores al diagnostico

Estos prompts estan preparados para usarse despues de obtener V1. No son evidencia de consultas ya ejecutadas ni sustituyen el diagnostico. Reemplaza los campos entre corchetes con datos reales del analisis.

## Revisar un hallazgo de seguridad o fiabilidad

> En el sistema Laravel de reclutamiento, SonarQube reporta la regla [regla], severidad [valor], archivo [ruta] y linea [linea]. Este es el codigo relevante: [fragmento sin secretos]. Explica el riesgo y como reproducirlo. Propone la correccion minima conservando organization_id, Policies, roles, auditoria append-only y decision humana RF-23. Si es un hotspot, distingue revision pendiente de vulnerabilidad confirmada. No cambies su estado sin evidencia. Antes de implementar una correccion funcional, agrega una prueba que falle con el defecto y pase con la solucion; incluye autorizacion y aislamiento cross-tenant cuando corresponda.

## Reducir complejidad o duplicacion

> El issue real [identificador] informa [regla] en [archivo:linea] con complejidad o duplicacion [valor observado]. Propone una refactorizacion limitada que conserve el comportamiento, transacciones, bloqueos, mensajes y contratos actuales. Explica el antes y el despues. Reutiliza las pruebas de regresion existentes y agrega solo casos que cubran riesgos del cambio. No excluyas codigo del analisis para reducir artificialmente la metrica.

## Mejorar cobertura

> La cobertura real de [archivo] es [valor], y SonarQube muestra estas lineas sin cubrir: [lineas]. Identifica reglas o caminos de error relevantes que no esten probados. Agrega pruebas de comportamiento significativas con datos ficticios, sin llamadas externas reales. Conserva PostgreSQL y RefreshDatabase para las pruebas de Laravel. No copies cobertura PHP como si fuera cobertura de TypeScript o Python. No elimines archivos del denominador ni fabriques aciertos en Clover.

## Redactar la comparacion final

> Compara los JSON y capturas autenticos de V1 y V2, sus commits y sus resultados de pruebas. Explica cada cambio, el issue real que lo motivo y su evidencia. Conserva los resultados que empeoraron y distingue pruebas omitidas, cobertura no disponible y ejecuciones fallidas. Relaciona los indicadores con el marco de calidad solicitado por el docente sin afirmar certificacion ISO. No atribuyas mejoras ni validacion con usuarios que no se realizaron.
