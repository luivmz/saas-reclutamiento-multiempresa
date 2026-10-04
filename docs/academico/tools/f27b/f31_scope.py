"""Excepciones de alcance exclusivas del delta F31 no confirmado.

Un registro Markdown persistente no concede permisos. Se exige la rama exacta y
el HEAD base aprobado; al confirmar F31 o cambiar de rama, la excepcion expira.
"""
import subprocess

F31_BRANCH = 'feature/f31-documentation-debt-cleanup'
F31_BASE = '2bf2a1eaba1d76bf7d45e0e9aa7887e6758d13e6'
GOVERNANCE = frozenset({'CLAUDE.md', 'README.md', 'docs/PROGRESS.md'})
PROTECTED_DELTA = frozenset({
    'docs/academico/practica-11/F11R_REGULARIZACION.md',
    'docs/academico/practica-11/F11_Arquitectura_del_Sistema_Colegio_Andino.docx',
    'docs/academico/practica-11/F11_Arquitectura_del_Sistema_Colegio_Andino.pdf',
    'docs/academico/practica-11/README.md',
    'docs/academico/practica-11/evidencias/README.md',
    'docs/academico/informe-final/F29H_Informe_Final_v1_Colegio_Andino.docx',
    'docs/academico/informe-final/F29H_Informe_Final_v1_Colegio_Andino.pdf',
    'docs/academico/informe-final/F29H_REGISTRO.md',
    'docs/academico/powerdesigner/F29_VALIDATION.md',
    'docs/academico/powerdesigner/MANIFEST.md',
    'docs/academico/powerdesigner/README.md',
    'docs/academico/powerdesigner/models/F29_UML_Academico.oom',
    'docs/academico/powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.png',
    'docs/academico/powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.svg',
    'docs/academico/powerdesigner/scripts/f29-arq01-arquitectura.ps1',
    'docs/academico/powerdesigner/scripts/f31-arq01-label-layout.ps1',
    'docs/academico/powerdesigner/scripts/f31-arq01-label-cleanup.ps1',
    'docs/academico/powerdesigner/scripts/make_f29_docs.py',
    'docs/academico/powerdesigner/scripts/validate_f29.py',
    'docs/academico/powerdesigner/validation/F31_ARQ01_label_cleanup.txt',
})


def active(root):
    branch = subprocess.run(['git', 'branch', '--show-current'], cwd=root,
                            capture_output=True, text=True)
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root,
                          capture_output=True, text=True)
    return (branch.returncode == head.returncode == 0
            and branch.stdout.strip() == F31_BRANCH and head.stdout.strip() == F31_BASE)
