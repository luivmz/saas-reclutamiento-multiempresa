# F29 — Vista F8 «F8 - Casos de Uso Academicos» en F29_UML_Academico.oom.
#
# Especificación: docs/academico/practica-08/POWERDESIGNER_PENDING.md (decisión del equipo
# de la F27D). Nombres: docs/academico/tools/f27b/m_cu.py (ACTORES, CU, INCLUDES,
# NOTA_AUDITORIA). 5 actores, CU-01 a CU-20 (sin CU-21), sin actor «Sistema».
#
# Disposición por áreas funcionales (A a E, las mismas del F5). Los actores con más casos
# (RR. HH. y Aprobador / Dirección) van a la derecha y sus casos en una sola columna; los
# demás actores, a la izquierda. La legibilidad se comprueba: ninguna línea atraviesa un
# símbolo ajeno.
#
# Requiere f29lib.ps1 cargado. Reemplaza el paquete F8 entero en cada corrida.

$ErrorActionPreference = 'Stop'
Open-F29
try {
    $m = Get-F29Model $F29Oom
    Write-Host "F8 - Casos de Uso Academicos en $($m.Name)"
    $v = Reset-OomView $m 'F8' 'F8 - Casos de uso (vista academica)' 'UseCaseDiagrams' 'F8 - Casos de Uso Academicos'
    $pk = $v.Package; $d = $v.Diagram
    $d.Comment = 'F8 Casos de uso - vista academica (CU-01 a CU-20). Formalizacion F29 de docs/academico/practica-08/POWERDESIGNER_PENDING.md. No sustituye ni edita UC-01 de la F23.'
    Set-DiagramFont $d 9

    $actors = @(
        @('ACT-01', 'Área solicitante', 0, 82000),
        @('ACT-04', 'Postulante', 0, 51500),
        @('ACT-05', 'Evaluador', 0, 32000),
        @('ACT-03', 'Aprobador / Dirección', 136000, 47000),
        @('ACT-02', 'Recursos Humanos', 132000, 35000)
    )
    $XR = 76000; $XL = 31000; $XM = 53000
    # id, nombre (Formato 08 aprobado), x, y, ancho
    $cases = @(
        @('CU-01', 'Registrar requerimiento de personal', $XL, 86000, 13000),
        @('CU-03', 'Aprobar o rechazar requerimiento', $XR, 86000, 13000),
        @('CU-02', 'Validar y corregir requerimiento', $XR, 80800, 13000),
        @('CU-04', 'Registrar perfil y criterios del puesto', $XR, 71000, 13000),
        @('CU-06', 'Publicar vacante', $XR, 65800, 13000),
        @('CU-05', 'Configurar y validar vacante', $XR, 60600, 13000),
        @('CU-07', 'Gestionar cuenta y acceso', $XL, 55000, 13000),
        @('CU-08', 'Gestionar perfil y CV', $XM, 51500, 13000),
        @('CU-09', 'Registrar postulación', $XL, 48000, 13000),
        @('CU-10', 'Consultar y revisar postulaciones', $XR, 42000, 13000),
        @('CU-11', 'Registrar preselección o descarte', $XR, 36800, 13000),
        @('CU-12', 'Gestionar cambio de etapa', $XR, 31600, 13000),
        @('CU-13', 'Programar evaluación', $XR, 26400, 13000),
        @('CU-14', 'Programar entrevista', $XR, 21200, 13000),
        @('CU-15', 'Registrar resultados de evaluación y entrevista', $XL, 32000, 15000),
        @('CU-16', 'Validar rangos y ponderaciones', $XM, 32000, 13000),
        @('CU-17', 'Consultar ranking y comparación', $XR, 15000, 13000),
        @('CU-18', 'Registrar decisión final humana', $XR, 9800, 13000),
        @('CU-19', 'Registrar selección', $XR, 4600, 13000),
        @('CU-20', 'Cerrar convocatoria y notificar resultado', $XR, -600, 13000)
    )
    $assoc = @{
        'ACT-01' = @('CU-01', 'CU-02')
        'ACT-02' = @('CU-02', 'CU-04', 'CU-05', 'CU-06', 'CU-10', 'CU-11', 'CU-12', 'CU-13', 'CU-14', 'CU-17', 'CU-19', 'CU-20')
        'ACT-03' = @('CU-03', 'CU-10', 'CU-17', 'CU-18')
        'ACT-04' = @('CU-07', 'CU-08', 'CU-09')
        'ACT-05' = @('CU-15')
    }
    $includes = @(@('CU-05', 'CU-16'), @('CU-15', 'CU-16'), @('CU-17', 'CU-16'))

    # Marcos de las áreas funcionales (se crean primero: quedan detrás de los casos).
    $areas = @(
        @('A. Requerimiento de personal', 90000, 77600),
        @('B. Convocatoria', 76600, 58600),
        @('C. Postulación', 58200, 45200),
        @('D. Evaluación', 44800, 18200),
        @('E. Selección y cierre', 17800, -3800)
    )
    Add-Frame $d 10000 94000 88000 -6500 | Out-Null
    Add-Text $d 'Plataforma SaaS de reclutamiento — vista académica de casos de uso (CU-01 a CU-20)' 11000 93600 88000 91000 | Out-Null
    foreach ($a in $areas) {
        Add-Frame $d 12000 $a[1] 86000 $a[2] 2 | Out-Null
        Add-Text $d $a[0] 12600 ($a[1] - 300) (12600 + 1200 + $a[0].Length * 430) ($a[1] - 2000) | Out-Null
    }

    $o = @{}; $s = @{}; $shapes = @()
    foreach ($a in $actors) {
        $x = $pk.CreateObject($OomKind.Actor)
        $x.Name = "$($a[0]) $($a[1])"; $x.Code = 'F8_' + ($a[0] -replace '-', '_')
        $o[$a[0]] = $x; $s[$a[0]] = $d.AttachObject($x)
        Set-Box $s[$a[0]] $a[2] $a[3] 2400 4000
        $shapes += [pscustomobject]@{ Id = $a[0]; X = $a[2]; Y = $a[3]; A = 1200; B = 2000; Ellipse = $false }
    }
    foreach ($c in $cases) {
        $x = $pk.CreateObject($OomKind.UseCase)
        $x.Name = "$($c[0]) $($c[1])"; $x.Code = 'F8_' + ($c[0] -replace '-', '_')
        $o[$c[0]] = $x; $s[$c[0]] = $d.AttachObject($x)
        Set-Box $s[$c[0]] $c[2] $c[3] $c[4] 4400
        $shapes += [pscustomobject]@{ Id = $c[0]; X = $c[2]; Y = $c[3]; A = $c[4] / 2; B = 2200; Ellipse = $true }
    }
    $o['CU-18'].Comment = 'Decision humana (RF-23): la registra solo el Aprobador / Direccion, con confirmacion explicita y justificacion. El ranking no elige.'
    $o['CU-17'].Comment = 'Calcula, ordena y compara; no selecciona.'

    $segments = @()
    foreach ($ak in $assoc.Keys) {
        foreach ($ck in $assoc[$ak]) {
            $l = $pk.CreateObject($OomKind.UseCaseAssociation)
            $l.Object1 = $o[$ak]; $l.Object2 = $o[$ck]
            $ls = $d.AttachLinkObject($l, $s[$ak], $s[$ck])
            $pts = Set-EdgeLink $ls $s[$ak] $s[$ck] $false $true
            $segments += [pscustomobject]@{ Name = "$ak-$ck"; Ends = @($ak, $ck); P1 = $pts[0]; P2 = $pts[1] }
        }
    }
    foreach ($inc in $includes) {
        $l = $pk.CreateObject($OomKind.Dependency)
        $l.Object1 = $o[$inc[0]]; $l.Object2 = $o[$inc[1]]; $l.Stereotype = 'include'
        $ls = $d.AttachLinkObject($l, $s[$inc[0]], $s[$inc[1]])
        $pts = Set-EdgeLink $ls $s[$inc[0]] $s[$inc[1]] $true $true
        $segments += [pscustomobject]@{ Name = "$($inc[0])>>$($inc[1])"; Ends = @($inc[0], $inc[1]); P1 = $pts[0]; P2 = $pts[1] }
    }

    # Notas obligatorias (a la izquierda de sus casos, en el área E, libre).
    Add-Note $d 'CU-17: calcula, ordena y compara; no selecciona.' 30000 16800 64000 13200 | Out-Null
    Add-Note $d 'CU-18: decisión humana (RF-23): la registra solo el Aprobador / Dirección; el ranking no elige.' 30000 12400 64000 7200 | Out-Null
    Add-Note $d 'Nota técnica de auditoría (no es un caso de uso): consulta de auditoría vinculada a RF-27 y ACT-03; cubierta por la vista técnica UC-RF27 y fuera del catálogo académico CU-01..CU-20 de esta versión.' 10000 -7500 88000 -11500 | Out-Null
    Add-Note $d 'El Sistema no es un actor: valida, calcula, notifica y audita dentro de los casos (inclusiones). Sin RF-29 ni actores fuera del alcance.' 10000 -12300 88000 -15300 | Out-Null
    Add-Text $d "F8 Casos de uso — vista académica (CU-01 a CU-20)`r`nCaso de estudio: Colegio Andino de Huancayo. Catálogo aprobado por el equipo (F27D). No sustituye a UC-01 (vista técnica, F23). Formalización F29 en PowerDesigner." 0 101000 130000 96000 | Out-Null

    # ================================================================ verificación
    $out = @(); $fail = @()
    $out += "F29 - verificación de la vista F8 - Casos de Uso Academicos ($(Get-Date -Format 'yyyy-MM-dd HH:mm'))"
    $out += "Modelo: docs/academico/powerdesigner/models/F29_UML_Academico.oom; paquete F8; diagrama «$($d.Name)»"
    $out += ''
    $acts = @($pk.GetCollectionByName('Actors')); $ucs = @($pk.GetCollectionByName('UseCases'))
    $out += "Actores: $($acts.Count) (5) · casos de uso: $($ucs.Count) (20)"
    if ($acts.Count -ne 5) { $fail += 'actores' }; if ($ucs.Count -ne 20) { $fail += 'casos' }
    if (@($acts | Where-Object { $_.Name -match 'Sistema' }).Count) { $fail += 'actor Sistema' }
    if (@($ucs | Where-Object { $_.Name -like 'CU-21*' }).Count) { $fail += 'CU-21 presente' }
    $cu18 = ($ucs | Where-Object { $_.Code -eq 'F8_CU_18' }).Name
    $out += "CU-18: «$cu18»"
    if ($cu18 -ne 'CU-18 Registrar decisión final humana') { $fail += 'nombre de CU-18' }
    # Matriz actor-caso y relaciones «include», leídas del modelo.
    $cid = { param($x) (($x.Code -replace '^F8_', '') -replace '_', '-') }
    $got = @(); $inc = @()
    foreach ($x in $pk.GetCollectionByName('UseCaseAssociations')) { $got += (& $cid $x.Object1) + '>' + (& $cid $x.Object2) }
    foreach ($x in $pk.GetCollectionByName('Dependencies')) { $inc += (& $cid $x.Object1) + '>' + (& $cid $x.Object2) + "<<$($x.Stereotype)>>" }
    $exp = @(); foreach ($ak in $assoc.Keys) { foreach ($ck in $assoc[$ak]) { $exp += "$ak>$ck" } }
    $d1 = Compare-Object ($exp | Sort-Object) ($got | Sort-Object)
    $d2 = Compare-Object (@('CU-05>CU-16<<include>>', 'CU-15>CU-16<<include>>', 'CU-17>CU-16<<include>>') | Sort-Object) ($inc | Sort-Object)
    $out += "Asociaciones actor-caso: $($got.Count) (esperadas $($exp.Count), matriz del Formato 08) · «include»: $($inc.Count) (3: CU-05, CU-15 y CU-17 -> CU-16) · «extend»: 0"
    if ($d1) { $fail += 'matriz: ' + (($d1 | ForEach-Object { $_.SideIndicator + $_.InputObject }) -join ' ') }
    if ($d2) { $fail += 'include: ' + (($d2 | ForEach-Object { $_.SideIndicator + $_.InputObject }) -join ' ') }
    $noActor = @($cases | Where-Object { $id = $_[0]; -not ($got | Where-Object { $_ -like "*>$id" }) } | ForEach-Object { $_[0] })
    $out += "Casos sin actor: $($noActor -join ', ') (CU-16 es inclusión, sin actor directo)"
    if (($noActor -join ',') -ne 'CU-16') { $fail += 'casos sin actor' }
    $hits = Test-LinkClearance $segments $shapes 400
    $out += "Legibilidad: $($segments.Count) líneas; líneas que atraviesan un símbolo ajeno: $($hits.Count)" + $(if ($hits.Count) { ' -> ' + ($hits -join '; ') })
    if ($hits.Count) { $fail += 'legibilidad' }
    $ck = Test-F29OomCheck $m
    $out += $ck.Lines
    if (-not $ck.Ok) { $fail += 'Check Model: hallazgos no explicados por la especificación' }
    # F29B: publicación reproducible (guardar, cerrar, reabrir, comparar geometría y
    # exportar desde el modelo reabierto; una segunda recarga debe reproducir el SVG).
    $pub = Publish-F29View $m 'F8' 'F8 - Casos de Uso Academicos' 'F8_Casos_de_Uso_Academicos' @()
    $out += $pub.Lines
    if (-not $pub.Ok) { $fail += 'reproducibilidad tras recarga' }
    $out += ''
    if ($fail.Count) { $out += 'RESULTADO: FALLA'; $out += $fail } else { $out += 'RESULTADO: PASS' }
    Write-F29Report (Join-Path $F29Root 'validation\F8_model_check.txt') $out
    $out | ForEach-Object { Write-Host "  $_" }
} finally { Close-F29 }
