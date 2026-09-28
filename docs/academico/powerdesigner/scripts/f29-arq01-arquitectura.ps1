# F29 — Vista ARQ-01 «ARQ-01 - Arquitectura Conceptual» en F29_UML_Academico.oom.
#
# Especificación: docs/academico/practica-11/POWERDESIGNER_PENDING.md (F28), con
# COMPONENTS.md (17 bloques) y RELATIONSHIPS.md (R-01 a R-20).
#
# Diagrama de componentes UML usado a nivel conceptual. Las 6 agrupaciones son paquetes
# UML que contienen sus componentes (conceptuales, no de despliegue) y se dibujan como
# contenedores; además se verifica que cada componente quede dentro de su contenedor.
# Los vínculos se llevan al frente: PowerDesigner dibuja los paquetes con relleno encima
# de los vínculos creados antes. Las relaciones con un marco (R-03, R-04, R-13, R-14 y R-16) apuntan al
# paquete «Capa de negocio». Los actores van en un paquete aparte, fuera del sistema, y se
# relacionan con C01 por una sola dependencia («usan»). C17 es experimental: borde
# discontinuo y solo R-19 y R-20, también discontinuas. No es CO-01, PK-01 ni DE-01.
#
# Requiere f29lib.ps1 cargado. Reemplaza el paquete ARQ01 entero en cada corrida.

$ErrorActionPreference = 'Stop'
Open-F29
try {
    $m = Get-F29Model $F29Oom
    Write-Host "ARQ-01 - Arquitectura Conceptual en $($m.Name)"
    $v = Reset-OomView $m 'ARQ01' 'ARQ-01 - Arquitectura conceptual (F11 adaptado)' 'ComponentDiagrams' 'ARQ-01 - Arquitectura Conceptual'
    $pk = $v.Package; $d = $v.Diagram
    $d.Comment = 'ARQ-01 Arquitectura conceptual del sistema (adaptacion academica de la Guia 11). Formalizacion F29 de docs/academico/practica-11/POWERDESIGNER_PENDING.md. No es un despliegue: ver DE-01.'
    # Los componentes pertenecen a sus paquetes: sin marca ni sufijo de acceso directo.
    Set-DisplayPref $d @{ 'Shortcut IntIcon' = 'No'; 'Shortcut IntLastPackage' = 'No'; 'Dependency.DisplayName' = 'Yes'; 'Package.TextStyle' = 'Yes' }
    Set-DiagramFont $d 9

    # ------------------------------------------------------------ agrupaciones (paquetes)
    # clave, nombre exacto, izquierda, arriba, derecha, abajo
    $groups = @(
        @('ACT', 'Actores (fuera del sistema)', -2000, 92000, 16000, 58000),
        @('PRE', 'Capa de presentación', 22000, 88000, 44000, 70000),
        @('ACC', 'Capa de acceso y seguridad', 50000, 88000, 98000, 70000),
        @('EXP', 'Experimental (opcional)', 108000, 88000, 138000, 70000),
        @('NEG', 'Capa de negocio', 22000, 62000, 138000, 30000),
        @('TRA', 'Servicios transversales', 22000, 25000, 116000, 11000),
        @('INF', 'Persistencia e infraestructura', 22000, 7000, 138000, -7000)
    )
    $gObj = @{}; $gSym = @{}
    foreach ($g in $groups) {
        $x = $pk.CreateObject($OomKind.Package)
        $x.Name = $g[1]; $x.Code = 'ARQ01_' + $g[0]
        if ($g[0] -ne 'ACT') { $x.Stereotype = 'conceptual' }
        $gObj[$g[0]] = $x
        $s = $d.AttachObject($x)
        Set-Rect $s $g[2] $g[3] $g[4] $g[5]
        $gSym[$g[0]] = $s
    }
    try { Set-P $gSym['EXP'] 'DashStyle' 2 } catch { Write-Warning 'Sin borde discontinuo en el paquete experimental' }

    # ------------------------------------------------------------ componentes (17)
    # id, nombre exacto (COMPONENTS.md), agrupación, estereotipo, x, y
    $comps = @(
        @('C01', 'Interfaz web', 'PRE', 'conceptual', 33000, 78000),
        @('C02', 'Autenticación y cuentas', 'ACC', 'conceptual', 60000, 78000),
        @('C03', 'Autorización y contexto multiempresa', 'ACC', 'conceptual, transversal', 88000, 78000),
        @('C17', 'Riesgo operacional del proceso (RF-29)', 'EXP', 'conceptual, experimental', 123000, 78000),
        @('C04', 'Requerimientos de personal', 'NEG', 'conceptual', 34000, 52000),
        @('C05', 'Vacantes y convocatorias', 'NEG', 'conceptual', 60000, 52000),
        @('C07', 'Postulaciones y etapas', 'NEG', 'conceptual', 86000, 52000),
        @('C06', 'Postulantes y CV', 'NEG', 'conceptual', 112000, 52000),
        @('C08', 'Evaluaciones y entrevistas', 'NEG', 'conceptual', 34000, 38000),
        @('C09', 'Ranking y comparación', 'NEG', 'conceptual, apoyo', 60000, 38000),
        @('C10', 'Decisión final humana', 'NEG', 'conceptual, human decision', 86000, 38000),
        @('C11', 'Selección y cierre', 'NEG', 'conceptual', 112000, 38000),
        @('C12', 'Notificaciones', 'TRA', 'conceptual, transversal', 40000, 18000),
        @('C13', 'Auditoría', 'TRA', 'conceptual, transversal', 100000, 18000),
        @('C16', 'Sesiones, caché y cola (Redis)', 'INF', 'conceptual, infraestructura', 40000, 0),
        @('C14', 'Persistencia de datos (PostgreSQL)', 'INF', 'conceptual, infraestructura', 100000, 0),
        @('C15', 'Almacenamiento privado de CV', 'INF', 'conceptual, infraestructura', 124000, 0)
    )
    $CW = 16000; $CH = 7000
    $c = @{}; $cs = @{}
    foreach ($k in $comps) {
        $x = $gObj[$k[2]].CreateObject($OomKind.Component)
        $x.Name = "$($k[0]) $($k[1])"; $x.Code = 'ARQ01_' + $k[0]; $x.Stereotype = $k[3]
        $x.Comment = 'Agrupacion: ' + ($groups | Where-Object { $_[0] -eq $k[2] })[1]
        $c[$k[0]] = $x
        $s = $d.AttachObject($x); Set-Box $s $k[4] $k[5] $CW $CH
        $cs[$k[0]] = $s
    }
    try { Set-P $cs['C17'] 'DashStyle' 2 } catch { Write-Warning 'Sin borde discontinuo en C17' }
    $c['C10'].Comment += '. Decision HUMANA (RF-23): la registra el Aprobador / Direccion con confirmacion y justificacion.'
    $c['C09'].Comment += '. Calcula, ordena y compara; no selecciona ni cambia estados.'
    $c['C17'].Comment += '. Experimental y opcional (RF-29): solo el proceso; no evalua personas; sin relacion con C09, C10 ni C11; desactivado por defecto.'

    # Actores: fuera del sistema, como un solo grupo relacionado con C01. Un diagrama de
    # componentes no admite símbolos de actor y los actores ya están definidos en el F8
    # (ACT-01 a ACT-05): el paquete los agrupa por nombre, sin duplicarlos.
    $acts = @('Área solicitante', 'Recursos Humanos', 'Aprobador / Dirección', 'Evaluador', 'Postulante')
    $gObj['ACT'].Comment = 'Grupo de actores de la vista ACT-01 a ACT-05 (definidos en el paquete F8). No forma parte de las 6 agrupaciones del sistema.'
    Move-ToFront $d (Add-Text $d ($acts -join "`r`n") -1000 84000 15000 62000)

    # ------------------------------------------------------------ relaciones
    function Rq($id) { if ($cs.ContainsKey($id)) { Get-Rect $cs[$id] } else { Get-Rect $gSym[$id] } }
    function Obj($id) { if ($c.ContainsKey($id)) { $c[$id] } else { $gObj[$id] } }
    function Sym($id) { if ($cs.ContainsKey($id)) { $cs[$id] } else { $gSym[$id] } }
    # id, origen, destino, rótulo, puntos (función), discontinua
    $rels = @(
        @('U', 'ACT', 'C01', 'usan', { @(@((Rq 'ACT').R, 78000), @((Rq 'C01').L, 78000)) }),
        @('R-01', 'C01', 'C02', 'credenciales / sesión', { @(@((Rq 'C01').R, 78000), @((Rq 'C02').L, 78000)) }),
        @('R-02', 'C02', 'C03', 'identidad, rol, organización', { @(@((Rq 'C02').R, 78000), @((Rq 'C03').L, 78000)) }),
        @('R-03', 'C03', 'NEG', 'autoriza y filtra por organización', { @(@(88000, (Rq 'C03').B), @(88000, (Rq 'NEG').T)) }),
        @('R-03b', 'C03', 'C13', 'autoriza y filtra por organización', { @(@(94000, (Rq 'C03').B), @(94000, 67500), @(143000, 67500), @(143000, 18000), @((Rq 'C13').R, 18000)) }),
        @('R-04', 'C01', 'NEG', 'uso (a través de C03)', { @(@(33000, (Rq 'C01').B), @(33000, (Rq 'NEG').T)) }),
        @('R-05', 'C04', 'C05', 'requerimiento aprobado', { @(@((Rq 'C04').R, 52000), @((Rq 'C05').L, 52000)) }),
        @('R-06', 'C05', 'C07', 'vacante publicada', { @(@((Rq 'C05').R, 52000), @((Rq 'C07').L, 52000)) }),
        @('R-07', 'C06', 'C07', 'perfil y CV', { @(@((Rq 'C06').L, 52000), @((Rq 'C07').R, 52000)) }),
        @('R-08', 'C08', 'C07', 'postulación elegible / avance de etapa', { @(@(34000, (Rq 'C08').T), @(34000, 45000), @(82000, 45000), @(82000, (Rq 'C07').B)) }),
        @('R-09', 'C08', 'C09', 'resultados realizados', { @(@((Rq 'C08').R, 38000), @((Rq 'C09').L, 38000)) }),
        @('R-10', 'C09', 'C10', 'comparación (apoyo; no elige)', { @(@((Rq 'C09').R, 38000), @((Rq 'C10').L, 38000)) }),
        @('R-11', 'C10', 'C11', 'decisión humana registrada', { @(@((Rq 'C10').R, 38000), @((Rq 'C11').L, 38000)) }),
        @('R-12', 'C11', 'C07', 'transiciones seleccionado / no seleccionado', { @(@(112000, (Rq 'C11').T), @(112000, 45000), @(90000, 45000), @(90000, (Rq 'C07').B)) }),
        @('R-13', 'NEG', 'C13', 'registro de acciones críticas', { @(@(100000, (Rq 'NEG').B), @(100000, (Rq 'C13').T)) }),
        @('R-14', 'NEG', 'C12', 'eventos de notificación', { @(@(40000, (Rq 'NEG').B), @(40000, (Rq 'C12').T)) }),
        @('R-15', 'C12', 'C16', 'encolado', { @(@(40000, (Rq 'C12').B), @(40000, (Rq 'C16').T)) }),
        @('R-16', 'NEG', 'C14', 'persistencia', { @(@(94000, (Rq 'NEG').B), @(94000, (Rq 'TRA').B + 600), @(94000, (Rq 'C14').T)) }),
        @('R-16b', 'C13', 'C14', 'persistencia', { @(@(104000, (Rq 'C13').B), @(104000, (Rq 'C14').T)) }),
        @('R-17', 'C06', 'C15', 'CV (escritura y descarga autorizada)', { @(@((Rq 'C06').R, 52000), @(124000, 52000), @(124000, (Rq 'C15').T)) }),
        @('R-17b', 'C07', 'C15', 'CV (escritura y descarga autorizada)', { @(@(86000, (Rq 'C07').T), @(86000, 57000), @(130000, 57000), @(130000, (Rq 'C15').T)) }),
        @('R-18', 'C02', 'C16', 'sesión', { @(@(58000, (Rq 'C02').B), @(58000, 67000), @(19000, 67000), @(19000, 0), @((Rq 'C16').L, 0)) }),
        @('R-19', 'C05', 'C17', '15 variables operacionales (opcional)', { @(@(60000, (Rq 'C05').T), @(60000, 65000), @(120000, 65000), @(120000, (Rq 'C17').B)) }, $true),
        @('R-20', 'C17', 'C01', 'información descriptiva de riesgo', { @(@(128000, (Rq 'C17').T), @(128000, 91000), @(27000, 91000), @(27000, (Rq 'C01').T)) }, $true)
    )
    $dep = @{}
    foreach ($r in $rels) {
        $x = $pk.CreateObject($OomKind.Dependency)
        $x.Object1 = Obj $r[1]; $x.Object2 = Obj $r[2]
        $label = $(if ($r[0] -eq 'U') { 'usan' } else { ($r[0] -replace 'b$', '') + ' ' + $r[3] })
        try { $x.Name = $label } catch { $x.Name = $label + ' ' }
        $x.Code = 'ARQ01_' + ($r[0] -replace '-', '_')
        $dep[$r[0]] = $x
        $ls = $d.AttachLinkObject($x, (Sym $r[1]), (Sym $r[2]))
        $lbl = @(0, 1); if ($r[0] -eq 'R-17') { $lbl = @(3000, -14000) }
        Set-LinkPoints $ls (& $r[4]) $lbl
        if ($r.Count -gt 5 -and $r[5]) { try { Set-P $ls 'DashStyle' 2 } catch {} } else { try { Set-P $ls 'DashStyle' 1 } catch {} }
        Move-ToFront $d $ls
    }

    # ------------------------------------------------------------ notas obligatorias y título
    Add-Note $d 'C17: experimental y opcional (RF-29): solo el proceso; no evalúa personas; sin relación con C09, C10 ni C11; desactivado por defecto.' 148000 88000 180000 78000 | Out-Null
    Add-Note $d 'C10: decisión HUMANA (RF-23): la registra el Aprobador / Dirección con confirmación y justificación.' 148000 46000 180000 38000 | Out-Null
    Add-Note $d 'C09: calcula, ordena y compara; no selecciona ni cambia estados.' 148000 36000 180000 30000 | Out-Null
    Add-Note $d 'Arquitectura conceptual (adaptación académica de la Guía 11). No es un despliegue: ver DE-01.' 148000 8000 180000 0 | Out-Null
    Add-Note $d 'Estereotipos: <<conceptual>> en todos los bloques; C03, C12 y C13 <<transversal>>; C09 <<apoyo>>; C10 <<human decision>>; C14 a C16 <<infraestructura>>; C17 <<experimental>> (borde y relaciones discontinuos). R-16 y R-17 tienen dos orígenes; R-03 dos destinos.' 148000 26000 180000 12000 | Out-Null
    Add-Text $d "ARQ-01 — Arquitectura conceptual del sistema`r`nSaaS multiempresa de reclutamiento, evaluación y selección — Colegio Andino de Huancayo. Adaptación académica (F11). Formalización F29 en PowerDesigner." -2000 100000 140000 95000 | Out-Null

    # ================================================================ verificación
    $out = @(); $fail = @()
    $out += "F29 - verificación de la vista ARQ-01 - Arquitectura Conceptual ($(Get-Date -Format 'yyyy-MM-dd HH:mm'))"
    $out += "Modelo: docs/academico/powerdesigner/models/F29_UML_Academico.oom; paquete ARQ01; diagrama «$($d.Name)»"
    $out += ''
    # Pertenencia: el centro de cada componente queda dentro del contenedor de su agrupación.
    $allComp = @()
    foreach ($x in @($groups | ForEach-Object { @($gObj[$_[0]].GetCollectionByName('Components')) })) {
        if (-not $x) { continue }
        $id = $x.Code -replace '^ARQ01_', ''
        $k = $comps | Where-Object { $_[0] -eq $id }
        $cc = Get-Center $cs[$id]; $gr = Get-Rect $gSym[$k[2]]
        $inside = $cc[0] -gt $gr.L -and $cc[0] -lt $gr.R -and $cc[1] -lt $gr.T -and $cc[1] -gt $gr.B
        if (-not $inside) { $fail += "$id fuera de su agrupación" }
        $allComp += [pscustomobject]@{ G = (Get-P (Get-P $x 'Parent') 'Name'); Name = $x.Name; Stereo = $x.Stereotype }
        if ((Get-P (Get-P $x 'Parent') 'Name') -ne ($groups | Where-Object { $_[0] -eq $k[2] })[1]) { $fail += "$id en otro paquete" }
    }
    $out += "Componentes: $($allComp.Count) (17) · agrupaciones: $(@($groups | Where-Object { $_[0] -ne 'ACT' }).Count) (6) · grupo de actores fuera del sistema: $($acts.Count) actores (los del F8), una sola relación «usan» con C01"
    if ($allComp.Count -ne 17) { $fail += 'componentes' }
    foreach ($k in $comps) { $x = $allComp | Where-Object { $_.Name -eq "$($k[0]) $($k[1])" }; if (-not $x) { $fail += "falta $($k[0])" } }
    if (@($allComp | Where-Object { $_.Name -like 'C18*' }).Count) { $fail += 'C18' }
    $out += 'Agrupación de cada componente: ' + (($allComp | ForEach-Object { ($_.Name -split ' ')[0] + '=' + $_.G }) -join '; ')
    $cid = { param($o) ($o.Code -replace '^ARQ01_', '') }
    $got = @(); foreach ($x in $pk.GetCollectionByName('Dependencies')) { $got += ((& $cid $x) -replace '_', '-') + ':' + (& $cid $x.Object1) + '>' + (& $cid $x.Object2) }
    $exp = @($rels | ForEach-Object { $_[0] + ':' + ($(if ($_[1] -in 'ACT', 'NEG') { $_[1] } else { $_[1] })) + '>' + $_[2] })
    $d1 = Compare-Object ($exp | Sort-Object) ($got | Sort-Object)
    $ids = @($rels | ForEach-Object { $_[0] -replace 'b$', '' } | Where-Object { $_ -ne 'U' } | Sort-Object -Unique)
    $out += "Relaciones: R-01 a R-20 presentes: $($ids.Count) (20) en $($got.Count) dependencias, incluida «usan» (R-03, R-16 y R-17 con dos trazos)"
    if ($d1) { $fail += 'relaciones: ' + (($d1 | ForEach-Object { $_.SideIndicator + $_.InputObject }) -join ' ') }
    if ($ids.Count -ne 20) { $fail += 'R-01..R-20' }
    $c17 = @($got | Where-Object { $_ -match 'C17' })
    $out += "Relaciones de C17: $($c17 -join ', ') (solo R-19 y R-20)"
    if ($c17.Count -ne 2 -or @($c17 | Where-Object { $_ -match 'C09|C10|C11' }).Count) { $fail += 'frontera de C17' }
    $chain = @('R-05:C04>C05', 'R-06:C05>C07', 'R-08:C08>C07', 'R-09:C08>C09', 'R-10:C09>C10', 'R-11:C10>C11', 'R-12:C11>C07')
    $out += 'Cadena principal C04 -> C05 -> C07 -> C08 -> C09 -> C10 -> C11 (y C11 -> C07): ' + $(if (@($chain | Where-Object { $got -notcontains $_ }).Count) { 'FALTA' } else { 'completa' })
    if (@($chain | Where-Object { $got -notcontains $_ }).Count) { $fail += 'cadena principal' }
    $forbid = @($allComp | Where-Object { $_.Name -match 'factura|suscrip|superadmin|talent|banco de talentos|kubernetes|meilisearch|nube|cloud|microservic|reporte|panel|RF-28|motor de selecci|API REST' })
    $out += "Elementos prohibidos (facturación, suscripciones, superadministración, banco de talentos, Kubernetes, Meilisearch, nube, API REST aparte, microservicios, reportes / RF-28, motor de selección): $($forbid.Count)"
    if ($forbid.Count) { $fail += 'prohibidos' }
    $ck = Test-F29OomCheck $m
    $out += $ck.Lines
    if (-not $ck.Ok) { $fail += 'Check Model: hallazgos no explicados por la especificación' }
    $out += ''
    if ($fail.Count) { $out += 'RESULTADO: FALLA'; $out += $fail } else { $out += 'RESULTADO: PASS' }
    Write-F29Report (Join-Path $F29Root 'validation\ARQ01_model_check.txt') $out
    $out | ForEach-Object { Write-Host "  $_" }

    Save-F29Model $m
    Export-F29 $d 'ARQ-01_Arquitectura_Conceptual'
} finally { Close-F29 }
