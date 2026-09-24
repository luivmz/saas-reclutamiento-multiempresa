"""Prepara el volcado del esquema para el lector 'PostgreSQL 9.x' de PowerDesigner 16.6.

Uso: python clean_schema.py <volcado-crudo.sql>

El volcado crudo se obtiene, fuera del repositorio, con
    docker compose exec postgres pg_dump --schema-only --no-owner --no-privileges -U <usuario> reclutamiento
y no se versiona. La salida es models/source/schema-postgresql.sql. La limpieza no
cambia el esquema: solo quita o traduce sintaxis que el lector PG9 no acepta.
"""
import io
import re
import sys
from pathlib import Path

BS = chr(92)
OUT = Path(__file__).resolve().parents[2] / 'models' / 'source' / 'schema-postgresql.sql'

s = io.open(sys.argv[1], encoding='utf-8').read()
lines = []
for line in s.splitlines():
    if line.startswith(BS + 'restrict') or line.startswith(BS + 'unrestrict'):
        continue
    if re.match(r'^SET ', line) or line.startswith('SELECT pg_catalog.set_config'):
        continue
    if re.match(r'^\s+AS (integer|bigint|smallint)\s*$', line):
        continue
    lines.append(line)

out = '\n'.join(lines)
out = out.replace('EXECUTE FUNCTION', 'EXECUTE PROCEDURE').replace('public.', '').replace('ALTER TABLE ONLY ', 'ALTER TABLE ')
out = re.sub(r'\n{3,}', '\n\n', out)

hdr = (
    "-- Esquema PostgreSQL del SaaS de reclutamiento (base reclutamiento, develop 2621bee).\n"
    "-- Origen: pg_dump --schema-only --no-owner --no-privileges del contenedor postgres (PostgreSQL 17.11).\n"
    "-- Limpieza para el parser 'PostgreSQL 9.x' de PowerDesigner 16.6, sin cambiar el esquema:\n"
    "--   quitadas las metaordenes restrict/unrestrict de psql y las lineas SET/set_config de sesion;\n"
    "--   quitado 'AS integer' de las secuencias (sintaxis PG10+);\n"
    "--   EXECUTE FUNCTION -> EXECUTE PROCEDURE en el trigger (equivalente en PG9);\n"
    "--   quitado el prefijo de esquema 'public.';\n"
    "--   ALTER TABLE ONLY -> ALTER TABLE (ONLY solo excluye tablas heredadas, que este esquema no tiene).\n"
    "-- Sin datos ni credenciales.\n\n"
)
io.open(OUT, 'w', encoding='utf-8', newline='\n').write(hdr + out.strip() + '\n')
print('tablas:', out.count('CREATE TABLE'), 'restrict:', out.count(BS + 'restrict'), 'SET:', len(re.findall(r'^SET ', out, re.M)))
