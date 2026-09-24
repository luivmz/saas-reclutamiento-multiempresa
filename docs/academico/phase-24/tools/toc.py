import re, json, sys
pages = open(sys.argv[1], encoding='utf8').read().split('=====PAGE ')[1:]
pages = {int(p.split('\n',1)[0]): p.split('\n',1)[1] for p in pages}
titles = ['1. Control del documento','2. Resumen ejecutivo','3. Contexto y problema','4. Objetivos del sistema',
 '5. Alcance incluido','6. Alcance excluido','7. Límites del sistema','8. Línea base funcional',
 '9. Línea base no funcional','10. Restricciones','11. Supuestos, dependencias y riesgos',
 '12. Criterios de aceptación del alcance','13. Trazabilidad del alcance','14. Control de cambios y conclusión']
res = {}
for tt in titles:
    for n in sorted(pages):
        if n <= 2: continue
        lines = [l.strip() for l in pages[n].splitlines()]
        if tt in lines:
            res[tt] = n; break
for n in sorted(pages):
    if n > 2 and any(l.strip().startswith('Anexo A.') for l in pages[n].splitlines()):
        res['Anexos A a F. Evidencia visual de referencia'] = n; break
print(json.dumps(res, ensure_ascii=False, indent=0))
missing = [t for t in titles if t not in res]
assert not missing, missing
json.dump(res, open(sys.argv[2], 'w'), ensure_ascii=False)
