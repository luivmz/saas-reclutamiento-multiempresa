# Resumen técnico ejecutivo (exposición de 5 a 10 minutos)

## 1. Problema (1 min)

En el análisis preliminar (AS-IS pendiente de validación), el reclutamiento del Colegio Andino de Huancayo presenta cinco problemas:

| # | Problema |
|---|---|
| P1 | Información distribuida |
| P2 | Seguimiento manual |
| P3 | Evaluaciones heterogéneas |
| P4 | Comunicación manual |
| P5 | Indicadores limitados |

Resultado: poca trazabilidad y comparaciones de candidatos difíciles de justificar.

## 2. Solución (1 min)

Una plataforma SaaS multiempresa que cubre el proceso completo en **27 requerimientos funcionales**:

```text
requerimiento → aprobación → vacante con criterios ponderados → postulación con CV
→ preselección → evaluación y entrevista → ranking explicable → DECISIÓN HUMANA
→ selección → cierre → notificación → auditoría
```

**Regla central:** el sistema calcula, ordena y compara; **la decisión final la toma el Aprobador/Dirección**, con justificación. Nunca hay selección automática.

## 3. Arquitectura y stack (1–2 min)

- **Estilo:** monolito modular multiempresa, sin microservicios.
- **Backend:** Laravel 13 (PHP 8.4).
- **Frontend:** React 19 + TypeScript + Inertia 3 + Tailwind 4.
- **Datos:** PostgreSQL 17, con integridad declarativa y auditoría de solo inserción.
- **Sesiones, caché y colas:** Redis 7 (worker de notificaciones).
- **Entorno:** Docker Compose.

**Multiempresa:**
- `organization_id` en las entidades, con *scope* global.
- Policies que verifican rol y organización en cada operación.
- El postulante tiene cuenta global y solo es visible para las organizaciones a cuyas vacantes postuló.
- RLS de PostgreSQL: mejora futura.

## 4. Flujo y roles (1 min)

| Rol | Hace |
|---|---|
| Área solicitante | Registra y envía requerimientos |
| RR. HH. | Valida, publica vacantes, gestiona etapas, programa sesiones, registra la selección y cierra |
| Aprobador / Dirección | Aprueba requerimientos, **toma la decisión final** y audita |
| Evaluador | Registra puntajes y resultados |
| Postulante | Perfil, CV, postulación y seguimiento |

## 5. Pruebas y calidad (2 min)

- **TDD:** RED observado → GREEN → REFACTOR, con evidencia por fase.
- **PHPUnit:** **244 pruebas**, **236 superadas**, **0 fallidas**, 8 omitidas del *starter kit*, 1074 aserciones.
  - Unitarias: ranking, estados, validadores.
  - *Feature*: los 27 RF, autorización y acceso entre organizaciones.
- **Cypress:** **14 specs, 43 tests, 43/43**, en entorno aislado y sin reintentos. Verde en corridas consecutivas y en una instalación limpia.
- **Defectos:** 13 registrados y 13 corregidos. Por ejemplo, la auditoría era modificable y se hizo de solo inserción con un *trigger*.
- **Portabilidad:** clon limpio → servicios *healthy* en 87 s → migraciones, *seed*, PHPUnit y Cypress en verde.
- **Cobertura de código:** no medida (se declara, no se inventa).

## 6. Resultados (30 s)

| Indicador | Valor |
|---|---|
| RF implementados y probados | 27 / 27 |
| PHPUnit | 236 / 236 ejecutadas en verde |
| Cypress | 43 / 43 |
| Defectos cerrados | 13 / 13 |
| Instalación reproducible | Validada |

## 7. Demo sugerida (3–5 min)

Guion completo en [demo-script.md](demo-script.md):
1. Ranking de «Auxiliar de Educación Inicial».
2. Decisión humana eligiendo al 2.º candidato.
3. Selección y cierre.
4. Notificación al postulante.
5. Auditoría.
6. `docker compose ps` y resultados de Cypress como evidencia.

## 8. Mensajes clave para cerrar

1. El ranking **ayuda** a decidir; la persona **decide**.
2. Cada RF está trazado a código, pruebas y evidencia.
3. Aislamiento entre organizaciones probado en backend y E2E.
4. El proyecto se instala y prueba desde cero en cualquier PC con Docker.
