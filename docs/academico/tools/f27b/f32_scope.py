"""Excepciones de navegacion vigentes autorizadas en la correccion F32-M01/L01.

Solo vale en la rama F32 y su HEAD base; expira al confirmar o cambiar de rama.
Solo permite README principal, dos README protegidos y su registro MANIFEST.
No permite runtime, binarios, otros documentos de gobierno ni cambios de permisos.
"""
import subprocess

F32_BRANCH = 'feature/f32-global-academic-audit'
F32_BASE = '70f4fcde47f81087024eefe60b6d42b45177cfef'
GOVERNANCE = frozenset({'README.md'})
PROTECTED_DELTA = frozenset({
    'docs/academico/powerdesigner/README.md',
    'docs/academico/powerdesigner/MANIFEST.md',
    'docs/academico/informe-final/README.md',
})


def active(root):
    branch = subprocess.run(['git', 'branch', '--show-current'], cwd=root,
                            capture_output=True, text=True)
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root,
                          capture_output=True, text=True)
    return (branch.returncode == head.returncode == 0
            and branch.stdout.strip() == F32_BRANCH and head.stdout.strip() == F32_BASE)
