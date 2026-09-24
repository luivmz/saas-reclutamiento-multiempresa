"""Extrae del esquema versionado las restricciones CHECK y el índice parcial.

Uso: python extract_checks.py <salida.json>

Lee models/source/schema-postgresql.sql. El lector 'PostgreSQL 9.x' de PowerDesigner
conserva un solo CHECK por tabla y pierde el WHERE del índice parcial; finish_pdm.ps1
usa este JSON para restituirlos en el PDM.
"""
import io
import json
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[2] / 'models' / 'source' / 'schema-postgresql.sql'
s = io.open(SRC, encoding='utf-8').read()

checks = {}
columns = 0
for m in re.finditer(r'CREATE TABLE (?:public\.)?(\w+) \((.*?)\n\);', s, re.S):
    table, body = m.group(1), m.group(2)
    for line in body.split('\n'):
        line = line.strip().rstrip(',')
        if not line:
            continue
        c = re.match(r'CONSTRAINT (\w+) CHECK \((.*)\)$', line)
        if c:
            checks.setdefault(table, []).append({'name': c.group(1), 'expr': c.group(2)})
        elif not line.startswith('CONSTRAINT'):
            columns += 1

idx = re.search(r'CREATE UNIQUE INDEX (\w+) ON (?:public\.)?(\w+) USING btree \((\w+)\) WHERE (.*);', s)
out = {
    'checks': checks,
    'check_total': sum(len(v) for v in checks.values()),
    'columns': columns,
    'partial_index': {'name': idx.group(1), 'table': idx.group(2), 'column': idx.group(3), 'where': idx.group(4)},
}
io.open(sys.argv[1], 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1))
print('tablas con CHECK:', len(checks), 'CHECK:', out['check_total'], 'columnas:', columns)
print('indice parcial:', out['partial_index'])
