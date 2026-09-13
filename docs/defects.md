# Registro de defectos reales

Solo se registran defectos efectivamente encontrados durante el desarrollo y las pruebas.

| ID | Defecto | Severidad | Detectado por | Estado | Corrección |
|---|---|---|---|---|---|
| DEF-01 | El contenedor `app` quedaba `unhealthy`: `php artisan serve` recarga `.env` en sus procesos hijos, por lo que `REDIS_HOST=127.0.0.1` sobrescribía la variable `REDIS_HOST=redis` de Docker Compose y fallaba la conexión a Redis (sesiones). | Alta | Healthcheck de Docker Compose (Iteración 1) | Cerrado | `.env.example` usa los hostnames de servicio (`postgres`, `redis`); `/health` se registra fuera del grupo `web` para no abrir sesión. |
| DEF-02 | 16 pruebas del starter kit fallaban dentro de Docker: `env_file: .env` inyectaba variables reales (`SESSION_DRIVER=redis`, `DB_DATABASE=reclutamiento`) que PHPUnit no sobrescribía, por lo que las pruebas corrían contra la base de desarrollo. | Crítica | `php artisan test` (Iteración 1) | Cerrado | Se eliminó `env_file` de `docker-compose.yml` (Laravel ya lee `.env`) y se agregó `force="true"` a las variables de `phpunit.xml`. Resultado posterior: 31 passed, 8 skipped. |
| DEF-03 | La creación de vacantes fallaba con `MassAssignmentException`: `JobProfile::firstOrNew(['vacancy_id' => …])` asignaba masivamente un atributo protegido. | Alta | `VacancyPublicationTest` (Iteración 2) | Cerrado | Búsqueda explícita del perfil y asignación directa de `vacancy_id`/`organization_id` en `VacancyService::saveProfile()`. |
| DEF-04 | El build de Vite y `tsc` fallaban: al desactivar la verificación de correo (A-01) Wayfinder dejó de generar `@/routes/verification`, pero `settings/profile.tsx` y `auth/verify-email.tsx` seguían importándolo. | Media | `npm run build` / `npm run types:check` (Iteración 2) | Cerrado | Se retiró el bloque de verificación del perfil, la página huérfana y la vista de Fortify asociada. |
