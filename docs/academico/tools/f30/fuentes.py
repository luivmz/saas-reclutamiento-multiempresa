"""F30 — Fuentes candidatas (identificador, DOI o URL, tema y origen).

Origen: «búsqueda» (conjunto cribado de busqueda_openalex.json, tema indicado), «bola de nieve» (citado por trabajos
seleccionados o fundacional del área) u «oficial» (norma, ley u organismo). Toda fuente se verifica con verificar.py
(Crossref o DataCite para DOI; respuesta HTTP para URL); la que no se verifica no entra en la matriz.
"""

# (id, doi, url, tema, origen)
FUENTES = [
    # --- A. IA en reclutamiento, ética y discriminación
    ('S01', '10.1145/3351095.3372828', None, 'A', 'búsqueda A'),
    ('S02', '10.1007/s40685-020-00134-w', None, 'A', 'búsqueda A'),
    ('S03', '10.1007/s10551-022-05049-6', None, 'A', 'búsqueda F'),
    ('S04', '10.1177/0008125619867910', None, 'A', 'bola de nieve'),
    ('S05', '10.1057/s41599-023-02079-x', None, 'A', 'búsqueda A'),
    ('S06', '10.1111/ijsa.12246', None, 'A', 'bola de nieve'),
    ('S07', '10.1037/apl0000695', None, 'T', 'bola de nieve'),
    ('S08', '10.1177/1529100619832930', None, 'T', 'bola de nieve'),
    ('S09', '10.1145/3442188.3445939', None, 'T', 'bola de nieve'),
    ('S10', '10.1073/pnas.1915768117', None, 'S', 'búsqueda T'),
    ('S11', '10.1609/aies.v7i1.31748', None, 'E', 'bola de nieve'),
    # --- C/D. Selección de personal, competencias y entrevistas estructuradas
    ('S12', '10.1037/0033-2909.124.2.262', None, 'D', 'bola de nieve'),
    ('S13', '10.1037/apl0000994', None, 'D', 'bola de nieve'),
    ('S14', '10.1037/0021-9010.79.4.599', None, 'D', 'búsqueda D'),
    ('S15', '10.1111/j.1744-6570.1997.tb00709.x', None, 'D', 'bola de nieve'),
    ('S16', '10.1111/peps.12052', None, 'D', 'bola de nieve'),
    ('S17', '10.1111/j.1744-6570.2010.01207.x', None, 'C', 'bola de nieve'),
    ('S18', '10.1146/annurev-psych-120710-100401', None, 'C', 'bola de nieve'),
    ('S19', '10.1037/h0047060', None, 'C', 'bola de nieve'),
    ('S20', '10.1037/0033-2909.86.2.420', None, 'C', 'bola de nieve'),
    ('S21', '10.1016/j.jcm.2016.02.012', None, 'C', 'bola de nieve'),
    ('S22', '10.1016/j.edurev.2018.12.003', None, 'C', 'bola de nieve'),
    ('S23', '10.1080/1359432x.2019.1681401', None, 'C', 'búsqueda C'),
    ('S24', '10.1037/0021-9010.86.5.897', None, 'D', 'búsqueda D'),
    # --- B/E/F/G/H. Ajuste persona-puesto, NLP, extracción y recomendación
    ('S25', '10.1145/3234465', None, 'B', 'búsqueda B'),
    ('S26', '10.1145/3209978.3210025', None, 'B', 'bola de nieve'),
    ('S27', '10.1007/s10115-020-01522-8', None, 'H', 'búsqueda H'),
    ('S28', '10.1145/3659942', None, 'H', 'búsqueda H'),
    ('S29', '10.18653/v1/2022.naacl-main.366', None, 'G', 'búsqueda G'),
    ('S30', '10.1109/access.2021.3106120', None, 'G', 'búsqueda G'),
    ('S31', '10.18653/v1/D19-1410', None, 'F', 'bola de nieve'),
    ('S32', '10.18653/v1/2020.acl-main.485', None, 'E', 'búsqueda E'),
    ('S33', '10.1162/tacl_a_00041', None, 'E', 'búsqueda E'),
    ('S34', '10.1145/3571730', None, 'E', 'bola de nieve'),
    ('S35', '10.1145/3442188.3445922', None, 'E', 'bola de nieve'),
    ('S36', '10.48550/arXiv.2306.05685', None, 'T', 'bola de nieve'),
    ('S37', '10.18653/v1/2021.acl-long.201', None, 'R', 'búsqueda R'),
    ('S38', '10.48550/arXiv.2212.04356', None, 'S', 'búsqueda S'),
    # --- I. Decisión multicriterio
    ('S39', '10.1016/0377-2217(90)90057-I', None, 'I', 'bola de nieve'),
    ('S40', '10.1016/j.eswa.2009.12.013', None, 'I', 'búsqueda I'),
    # --- K. Equidad y sesgo
    ('S41', '10.1145/3457607', None, 'K', 'búsqueda K'),
    ('S42', '10.15779/Z38BG31', None, 'K', 'bola de nieve'),
    ('S43', '10.48550/arXiv.1610.02413', None, 'K', 'bola de nieve'),
    ('S44', '10.4230/LIPIcs.ITCS.2017.43', None, 'K', 'bola de nieve'),
    ('S45', '10.1089/big.2016.0047', None, 'K', 'bola de nieve'),
    ('S46', '10.1145/3287560.3287589', None, 'K', 'búsqueda K'),
    ('S47', '10.1145/3465416.3483305', None, 'K', 'bola de nieve'),
    ('S48', '10.1126/science.aax2342', None, 'K', 'búsqueda A'),
    ('S49', '10.1147/JRD.2019.2942287', None, 'K', 'bola de nieve'),
    ('S50', '10.1145/3290605.3300830', None, 'K', 'bola de nieve'),
    # --- J. Explicabilidad
    ('S51', '10.1038/s42256-019-0048-x', None, 'J', 'bola de nieve'),
    ('S52', '10.1145/2939672.2939778', None, 'J', 'bola de nieve'),
    ('S53', '10.48550/arXiv.1705.07874', None, 'J', 'bola de nieve'),
    ('S54', '10.2139/ssrn.3063289', None, 'J', 'bola de nieve'),
    ('S55', '10.1016/j.artint.2018.07.007', None, 'J', 'búsqueda J'),
    ('S56', '10.1145/3351095.3375624', None, 'J', 'búsqueda P'),
    # --- M. Humano en el circuito
    ('S57', '10.1145/3287560.3287563', None, 'M', 'bola de nieve'),
    ('S58', '10.1145/3411764.3445717', None, 'M', 'bola de nieve'),
    ('S59', '10.1145/3579605', None, 'M', 'búsqueda M'),
    ('S60', '10.1038/s41562-024-02024-1', None, 'M', 'búsqueda M'),
    ('S61', '10.1093/jopart/muac007', None, 'M', 'búsqueda M'),
    ('S62', '10.1145/3290605.3300233', None, 'M', 'bola de nieve'),
    ('S63', '10.1177/0018720810376055', None, 'M', 'bola de nieve'),
    # --- N. Incertidumbre, calibración y métricas
    ('S64', '10.1145/1102351.1102430', None, 'N', 'bola de nieve'),
    ('S65', '10.48550/arXiv.1706.04599', None, 'N', 'búsqueda N'),
    ('S66', '10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2', None, 'N', 'bola de nieve'),
    ('S67', '10.1007/s10994-023-06336-7', None, 'N', 'búsqueda N'),
    ('S68', '10.1371/journal.pone.0118432', None, 'N', 'bola de nieve'),
    ('S69', '10.1145/582415.582418', None, 'N', 'bola de nieve'),
    ('S70', '10.1007/s10994-021-05946-3', None, 'N', 'búsqueda N'),
    # --- O/P/L. Gobernanza, auditoría, documentación y MLOps
    ('S71', '10.1145/3287560.3287596', None, 'P', 'bola de nieve'),
    ('S72', '10.1145/3458723', None, 'P', 'bola de nieve'),
    ('S73', '10.1145/3351095.3372873', None, 'P', 'búsqueda L'),
    ('S74', '10.1145/2382577.2382579', None, 'O', 'bola de nieve'),
    ('S75', '10.1145/2523813', None, 'O', 'búsqueda O'),
    ('S76', '10.1109/BigData.2017.8258038', None, 'O', 'bola de nieve'),
    ('S77', '10.1109/access.2023.3262138', None, 'O', 'búsqueda O'),
    ('S78', '10.1145/3533378', None, 'O', 'búsqueda O'),
    ('S79', '10.1145/3442188.3445918', None, 'P', 'búsqueda P'),
    ('S80', '10.1080/0960085x.2021.1927213', None, 'Q', 'búsqueda Q'),
    # --- Complementos de 2021–2025 localizados en una segunda búsqueda (Crossref / OpenAlex)
    ('S81', '10.1145/3630106.3658996', None, 'S', 'búsqueda complementaria'),
    ('S82', '10.1007/s10869-023-09874-y', None, 'T', 'búsqueda complementaria'),
    ('S83', '10.1145/3689904.3694699', None, 'E', 'búsqueda complementaria'),
    ('S84', '10.1609/aies.v8i3.36749', None, 'M', 'búsqueda complementaria'),
    ('S85', '10.1145/3462244.3479897', None, 'T', 'búsqueda complementaria'),
    ('S86', '10.1111/peps.12578', None, 'D', 'búsqueda complementaria'),
    ('S87', '10.1145/3630106.3658933', None, 'E', 'búsqueda complementaria'),
    ('S88', '10.21437/interspeech.2023-105', None, 'S', 'búsqueda complementaria'),
    ('S89', '10.1111/peps.12608', None, 'C', 'búsqueda complementaria'),
    # --- Documentos oficiales y normas
    ('O01', None, 'https://eur-lex.europa.eu/eli/reg/2024/1689/oj', 'L', 'oficial'),
    ('O02', None, 'https://eur-lex.europa.eu/eli/reg/2016/679/oj', 'L', 'oficial'),
    ('O03', '10.6028/NIST.AI.100-1', None, 'L', 'búsqueda L'),
    ('O04', '10.6028/NIST.SP.1270', None, 'K', 'búsqueda A'),
    ('O05', None, 'https://www.iso.org/standard/42001', 'L', 'oficial'),
    ('O06', None, 'https://www.iso.org/standard/77304.html', 'L', 'oficial'),
    ('O07', None, 'https://oecd.ai/en/ai-principles', 'L', 'oficial'),
    ('O08', None, 'https://www.unesco.org/en/artificial-intelligence/recommendation-ethics', 'L', 'oficial'),
    ('O09', None, 'https://www.gob.pe/institucion/smv/normas-legales/6426760-016-2024-jus', 'L', 'oficial'),
    ('O10', None, 'https://www.gob.pe/institucion/congreso-de-la-republica/normas-legales/4565760-31814', 'L', 'oficial'),
    ('O11', None, 'https://www.govinfo.gov/content/pkg/CFR-2017-title29-vol4/xml/CFR-2017-title29-vol4-part1607.xml', 'K', 'oficial'),
    ('O12', None, 'https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page', 'A', 'oficial'),
    ('O13', None, 'https://www.gob.pe/institucion/pcm/normas-legales/7133522-115-2025-pcm', 'L', 'oficial'),
    ('O14', None, 'https://www.gob.pe/institucion/minedu/informes-publicaciones/3280180-marco-del-buen-desempeno-docente', 'C', 'oficial'),
    # Añadidas en la corrección de auditoría F30 (L02 y M03)
    ('O15', None, 'https://www.gob.pe/institucion/congreso-de-la-republica/normas-legales/243470-29733', 'L', 'oficial'),
    ('O16', None, 'https://eur-lex.europa.eu/eli/reg/2026/1744/oj', 'L', 'oficial'),
    # --- Fuentes secundarias (solo contexto o verificación de texto normativo; no fundamentan decisiones solas)
    ('X01', None, 'https://artificialintelligenceact.eu/annex/3/', 'L', 'secundaria'),
    ('X02', None, 'https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/', 'L', 'secundaria'),
]

# Palabra que debe aparecer en el título (o, para XML, en el contenido) de cada página oficial: evita aceptar una URL
# que responde 200 pero lleva a otro documento. EUR-Lex responde 202 a clientes automáticos (página de verificación):
# para esas fuentes se descarga el texto oficial del Diario Oficial desde la Oficina de Publicaciones de la UE (Cellar,
# CELEX_OFICIAL) y se exige el número del reglamento en él. Cuando EUR-Lex sí responde 200, se exige en el título.
CLAVE_URL = {
    'O01': '2024/1689', 'O02': '2016/679', 'O05': '42001', 'O06': '23894', 'O07': 'AI Principles',
    'O08': 'Ethics of Artificial Intelligence',
    'O09': '016-2024-JUS', 'O10': '31814', 'O11': 'UNIFORM GUIDELINES ON EMPLOYEE SELECTION', 'O12': 'Automated Employment',
    'O13': '115-2025-PCM', 'O14': 'Buen Desempeño Docente', 'O15': '29733', 'O16': '2026/1744', 'X01': 'Annex III',
    'X02': 'Omnibus',
}
ELI_202 = {'O01', 'O02', 'O16'}
# Texto oficial (Oficina de Publicaciones de la UE) de las normas de EUR-Lex, por número CELEX.
CELEX_OFICIAL = {'O01': '32024R1689', 'O02': '32016R0679', 'O16': '32026R1744'}
