# Errata del preregistro EXP-BM25-LEXICO-v1 (12/11/2026)

> **EXPERIMENTAL — rama local `exp/evidencias-ml02`.** Corrige una descripción del [preregistro](PREREGISTRO_EXP-BM25-LEXICO-v1.md), que se conserva sin cambios, tal como se versionó en `e3f80a157af8c56e0d89bff997d3c7e26f68722a`. No cambia el método, sus parámetros ni sus resultados, y no habilita nada: F37-SBX y F38-SBX siguen BLOQUEADAS.

## Qué se corrige (APP-L02)

El preregistro dice, en la fila «Análisis» de su §1, que el método elimina «una lista fija de **51** palabras vacías». La lista real tiene **49**.

| Dato | Valor |
|---|---|
| Fuente | `TextAnalyzer::STOPWORDS`, en `app/Services/Ml02/TextAnalyzer.php` |
| Blob de ese archivo | `3196300c6b19f5f17fa6928f6846b9a371839cc2`, idéntico en `e3f80a1` (preregistro y método) y en los commits posteriores de la rama |
| Literales | 49, sin repetidos |
| Lista | a, al, ante, con, como, de, del, e, el, en, entre, es, esa, ese, eso, esta, estas, este, esto, estos, fue, la, las, le, les, lo, los, mas, muy, ni, no, o, para, por, que, se, sin, sobre, son, su, sus, u, un, una, unas, uno, unos, y, ya |

Lo detectó la auditoría de Codex del 10/11/2026, y se volvió a contar el 12/11/2026 sobre los dos commits.

## Qué no cambia

- **El método.** El método que se ejecutó y se preregistró es el código de `e3f80a1`, identificado por sus clases y su commit. La cifra 51 era un error de redacción.
- **El código.** No se añaden dos palabras al código para que coincida con el texto: el método ya se ejecutó sobre `test`, y cambiarlo exigiría un `method_id` nuevo y otro preregistro (§2 del preregistro).
- **Los resultados.** Se conservan tal como salieron, en [`RESULTADOS.md`](../resultados-exp-bm25-v1/RESULTADOS.md):

  | Partición | Recall@3 |
  |---|---|
  | `dev` | 0,5 |
  | `test` | 0 |

  H2 queda rechazada.
