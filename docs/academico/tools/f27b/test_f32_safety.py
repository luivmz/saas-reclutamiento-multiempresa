"""Regresion F32: dispatcher sin escrituras historicas y excepcion Git acotada.

Los builders se sustituyen por mocks: ninguna prueba regenera entregables.
"""
import importlib
import subprocess
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import build


class BuildSafetyTests(unittest.TestCase):
    def setUp(self):
        self.builders = {'f3': Mock(), 'f11': Mock(), 'f11r': Mock()}

    def test_default_excludes_historical_and_keeps_official(self):
        with patch.dict(build.BUILDERS, self.builders, clear=True):
            self.assertEqual(build.resolve_builder_keys([]), ['f3', 'f11r'])

    def test_historical_key_rejected_before_any_builder(self):
        with patch.dict(build.BUILDERS, self.builders, clear=True):
            with self.assertRaisesRegex(SystemExit, 'f11r'):
                build.main(['f3', 'f11'])
        for fn in self.builders.values():
            fn.assert_not_called()

    def test_direct_historical_call_fails_before_diagram(self):
        with patch.object(build, 'arch_diagram', side_effect=AssertionError('historic write path reached')) as diagram:
            with self.assertRaisesRegex(ValueError, 'f11r'):
                build.build_f11()
        diagram.assert_not_called()

    def test_default_dispatch_never_calls_historical(self):
        with patch.dict(build.BUILDERS, self.builders, clear=True):
            build.main([])
        self.builders['f3'].assert_called_once_with()
        self.builders['f11r'].assert_called_once_with()
        self.builders['f11'].assert_not_called()

    def test_explicit_official_dispatch_only_calls_official(self):
        with patch.dict(build.BUILDERS, self.builders, clear=True):
            build.main(['f11r'])
        self.builders['f11r'].assert_called_once_with()
        self.builders['f3'].assert_not_called()
        self.builders['f11'].assert_not_called()

    def test_unknown_key_rejected_before_any_builder(self):
        with patch.dict(build.BUILDERS, self.builders, clear=True):
            with self.assertRaisesRegex(SystemExit, 'desconocida'):
                build.main(['f3', 'unknown'])
        for fn in self.builders.values():
            fn.assert_not_called()

    def test_adapted_artifacts_unchanged_from_head(self):
        root = Path(build.ROOT)
        stem = 'docs/academico/practica-11/F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino'
        paths = [stem + ext for ext in ('.docx', '.pdf', '.md')]
        self.assertTrue(all((root / path).is_file() for path in paths))
        result = subprocess.run(['git', 'diff', '--quiet', 'HEAD', '--', *paths], cwd=root)
        self.assertEqual(result.returncode, 0, 'Los artefactos F11 historicos deben permanecer intactos')


class F32ScopeTests(unittest.TestCase):
    def test_only_readme_is_authorized(self):
        scope = importlib.import_module('f32_scope')
        self.assertEqual(scope.GOVERNANCE, frozenset({'README.md'}))
        self.assertEqual(scope.PROTECTED_DELTA, frozenset({
            'docs/academico/powerdesigner/README.md',
            'docs/academico/powerdesigner/MANIFEST.md',
            'docs/academico/informe-final/README.md',
        }))

    def test_exact_branch_and_base_required(self):
        scope = importlib.import_module('f32_scope')
        for branch, head, expected in (
            (scope.F32_BRANCH, scope.F32_BASE, True),
            ('feature/another-phase', scope.F32_BASE, False),
            (scope.F32_BRANCH, '0' * 40, False),
        ):
            with self.subTest(branch=branch, head=head):
                with patch.object(scope.subprocess, 'run', side_effect=[
                    SimpleNamespace(returncode=0, stdout=branch + '\n'),
                    SimpleNamespace(returncode=0, stdout=head + '\n'),
                ]):
                    self.assertEqual(scope.active('.'), expected)

    def test_git_failure_never_authorizes(self):
        scope = importlib.import_module('f32_scope')
        with patch.object(scope.subprocess, 'run', side_effect=[
            SimpleNamespace(returncode=1, stdout=scope.F32_BRANCH),
            SimpleNamespace(returncode=0, stdout=scope.F32_BASE),
        ]):
            self.assertFalse(scope.active('.'))


if __name__ == '__main__':
    unittest.main()
