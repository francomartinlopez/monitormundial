#!/usr/bin/env python3
"""Genera datos-informe.json (raíz del sitio) para la web de informes de Plexum.

Formato: "Datos que cada web publica para la web de informes de Plexum", v1.2, parte común y
apartado 9 (Monitor Mundial · Economía internacional). Sale solo de lo que ya está en
datos/semana.json: no se inventa ni se estima nada. No cambia nada visible del sitio.

Uso: python3 scripts/datos_informe.py   (después de cargar la semana y de scripts/indice_adr.py)
"""
import calendar, datetime as dt, json, os, re, unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEMANA = os.path.join(RAIZ, 'datos', 'semana.json')
SALIDA = os.path.join(RAIZ, 'datos-informe.json')
SITIO = 'https://francomartinlopez.github.io/monitormundial/'
TZ = dt.timezone(dt.timedelta(hours=-3))
EJE = 'Economía internacional'
ARG = {'nivel': 'nacional', 'provincia': '', 'localidad': '', 'pais': 'Argentina'}
MUNDO = {'nivel': 'mundo', 'provincia': '', 'localidad': '', 'pais': ''}

def pais(p): return {'nivel': 'país', 'provincia': '', 'localidad': '', 'pais': p}

# Indicadores del apartado 9: clave en semana.json → cómo se publica.
# (id estable, nombre, clave en valores, alcance, rubros, subrubros, exposicion, ancla del sitio)
IND = [
    ('riesgo-pais-argentina', 'Riesgo país (EMBI Argentina)', 'riesgo-pais-argentina', ARG, [], [], ['Deuda en dólares'], 'economia'),
    ('merval-pesos', 'Merval en pesos (MSCI Merval)', 'merval-pesos', ARG, [], [], [], 'economia'),
    ('merval-dolares', 'Merval en dólares (CCL)', 'merval-usd', ARG, [], [], [], 'economia'),
    ('indice-adr-argentinos', 'Índice de ADR argentinos (base 31/12/2025 = 100)', 'indice-adr', ARG, [], [], [], 'economia'),
    ('petroleo-brent', 'Petróleo Brent', 'brent', MUNDO, ['Energía'], ['petróleo'], ['Energía intensiva'], 'economia'),
    ('soja-chicago', 'Soja (Chicago)', 'soja-poroto', MUNDO, ['Agro'], ['soja'], ['Exporta'], 'economia'),
    ('maiz-chicago', 'Maíz (Chicago)', 'maiz', MUNDO, ['Agro'], ['maíz'], ['Exporta'], 'economia'),
    ('trigo-chicago', 'Trigo (Chicago)', 'trigo', MUNDO, ['Agro'], ['trigo'], ['Exporta'], 'economia'),
    ('soja-fob-argentina', 'Soja FOB oficial (puertos argentinos)', 'fob-soja-rosario', ARG, ['Agro'], ['soja'], ['Exporta'], 'economia'),
    ('harina-soja-fob-argentina', 'Harina de soja FOB', 'fob-harina-soja-rosario', ARG, ['Agro', 'Industria'], ['harina de soja'], ['Exporta'], 'economia'),
    ('aceite-soja-fob-argentina', 'Aceite de soja FOB Up River', 'fob-aceite-soja-rosario', ARG, ['Agro', 'Industria'], ['aceite de soja'], ['Exporta'], 'economia'),
    ('maiz-fob-argentina', 'Maíz FOB oficial (puertos argentinos)', 'fob-maiz-rosario', ARG, ['Agro'], ['maíz'], ['Exporta'], 'economia'),
    ('trigo-fob-argentina', 'Trigo FOB oficial (puertos argentinos)', 'fob-trigo-rosario', ARG, ['Agro'], ['trigo'], ['Exporta'], 'economia'),
    ('real-por-dolar', 'Real brasileño por dólar (nominal)', 'real-por-dolar', pais('Brasil'), [], [], ['Exporta', 'Importa insumos'], 'economia'),
    ('yuan-por-dolar', 'Yuan por dólar (nominal)', 'yuan-por-dolar', pais('China'), [], [], ['Exporta', 'Importa insumos'], 'economia'),
    ('indice-dolar-dxy', 'Índice del dólar (DXY)', 'indice-dolar-dxy', pais('Estados Unidos'), [], [], ['Deuda en dólares'], 'economia'),
    ('actividad-brasil', 'Actividad económica de Brasil (IBC-Br, variación mensual)', 'actividad-brasil', pais('Brasil'), ['Industria'], [], ['Exporta'], 'economia'),
]
# Indicadores del apartado que el sitio no muestra: van siempre a faltantes.
NO_MUESTRA = [
    ('acero', 'Precio internacional del acero', 'El sitio no publica un precio del acero; las medidas sobre el acero están en las barreras comerciales.'),
    ('tipo-cambio-real-brasil', 'Tipo de cambio real con Brasil', 'El sitio muestra el tipo de cambio nominal (real por dólar), no el tipo de cambio real bilateral.'),
    ('tipo-cambio-real-china', 'Tipo de cambio real con China', 'El sitio muestra el tipo de cambio nominal (yuan por dólar), no el tipo de cambio real bilateral.'),
    ('tipo-cambio-real-eeuu', 'Tipo de cambio real con EE. UU.', 'El sitio no publica el tipo de cambio real bilateral con EE. UU.'),
]
SECTOR = {'Energía': (['Energía'], ['petróleo y gas']), 'Bancos': (['Comercio y servicios'], ['bancos']),
          'Inmobiliario': (['Construcción'], ['inmobiliario']), 'Agro e inmobiliario': (['Agro', 'Construcción'], ['agro e inmobiliario']),
          'Fundadas en Argentina': (['Comercio y servicios'], ['tecnología'])}
OTRAS = {'TEO': (['Comercio y servicios'], ['telecomunicaciones']), 'LOMA': (['Construcción', 'Industria'], ['cemento']),
         'CAAP': (['Comercio y servicios'], ['aeropuertos'])}
PAISES = {'EE.UU.': 'Estados Unidos', 'UE': 'Unión Europea', 'UE–Mercosur': 'Unión Europea', 'EE.UU.–Argentina': 'Estados Unidos'}
RUBRO_CLAVES = [('Agro', r'soja|maíz|trigo|carne|grano|miel|cítric|limón|vino|aceite|harina|biodiésel|cuero|alimento|lácte'),
                ('Industria', r'acero|alumin|tubo|industria|auto|químic|manufact|biodiésel'),
                ('Minería', r'litio|cobre|oro|plata|miner'), ('Energía', r'petróleo|gas|energ|biodiésel|combustible'),
                ('Construcción', r'cemento|construcc')]

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def num(x):
    if isinstance(x, (int, float)): return x
    return None

def fin_mes(periodo):
    a, m = map(int, periodo.split('-'))
    return f'{a:04d}-{m:02d}-{calendar.monthrange(a, m)[1]:02d}'

def variacion(v):
    d = v.get('d')
    if not isinstance(d, (int, float)): return None
    uni = {'pct': '%', 'pb': 'p. b.', 'pp': 'p. p.'}.get(v.get('dt'), v.get('u', ''))
    return {'valor': d, 'unidad': uni, 'contra': v.get('d_contra') or 'semana anterior'}

def resumen60(*textos):
    t = ' '.join(x.strip() for x in textos if x).replace('Lectura propia.', '').strip()
    pal = t.split()
    if len(pal) <= 60: return t
    corto = ' '.join(pal[:60])
    k = corto.rfind('. ')
    return corto[:k + 1] if k > 80 else corto.rstrip(',;:') + '…'

def rubros_de(texto):
    r = [n for n, pat in RUBRO_CLAVES if re.search(pat, texto, re.I)]
    return r

def main():
    d = json.load(open(SEMANA))
    V = d['valores']
    corte = dt.date.fromisoformat(d['adr']['corte']) if d.get('adr', {}).get('corte') else dt.date.today()
    hoy = dt.datetime.now(TZ)
    indicadores, faltantes = [], []

    for iid, nombre, clave, alc, rub, sub, expo, ancla in IND:
        v = V.get(clave)
        if not v or (num(v.get('v')) is None and not (isinstance(v.get('v'), str) and v['v'].strip() not in ('', '—'))) or not v.get('fecha'):
            faltantes.append({'id': iid, 'nombre': nombre, 'motivo': (v or {}).get('nota', 'Sin dato publicado en el sitio.')[:200] if v else 'Sin dato publicado en el sitio.',
                              'ultimo_dato': None})
            continue
        periodo = v.get('periodo')
        reg = {'id': iid, 'nombre': nombre, 'valor': v['v'], 'unidad': v.get('u', ''),
               'fecha_dato': fin_mes(periodo) if periodo else v['fecha']}
        var = variacion(v)
        if var: reg['variacion'] = var
        if periodo: reg['periodo'] = periodo
        reg.update({'fuente_original': v.get('f', ''), 'eje': EJE, 'alcance': alc, 'rubros': rub, 'subrubros': sub,
                    'exposicion': expo, 'url': v.get('url') or SITIO + '#' + ancla})
        indicadores.append(reg)

    for a in d.get('adr', {}).get('acciones', []):
        iid = 'adr-' + a['ticker'].lower()
        if not isinstance(a.get('cierre'), (int, float)):
            faltantes.append({'id': iid, 'nombre': f"ADR {a['nombre']} ({a['ticker']})", 'motivo': 'Sin cierre del viernes en el sitio.', 'ultimo_dato': None})
            continue
        rub, sub = OTRAS.get(a['ticker']) or SECTOR.get(a['sector'], ([], []))
        reg = {'id': iid, 'nombre': f"ADR {a['nombre']} ({a['ticker']}, Nueva York)", 'valor': a['cierre'], 'unidad': 'USD',
               'fecha_dato': d['adr']['corte']}
        if isinstance(a.get('var_sem'), (int, float)):
            reg['variacion'] = {'valor': a['var_sem'], 'unidad': '%', 'contra': 'viernes anterior'}
        reg.update({'fuente_original': a.get('f', ''), 'eje': EJE, 'alcance': ARG, 'rubros': rub, 'subrubros': sub,
                    'exposicion': [], 'url': a.get('url') or SITIO + '#economia'})
        indicadores.append(reg)

    for iid, nombre, motivo in NO_MUESTRA:
        faltantes.append({'id': iid, 'nombre': nombre, 'motivo': motivo, 'ultimo_dato': None})

    # Novedades: medidas comerciales que afectan a la Argentina (últimos 90 días).
    novedades, vistos = [], set()
    limite = corte - dt.timedelta(days=90)
    fichas = [(f, True) for f in d['fichas'].get('barreras', [])] + [(f, False) for f in d['fichas'].get('comercio', [])]
    for f, es_barrera in fichas:
        c = f.get('campos', {})
        texto = ' '.join([f.get('nombre', '')] + [str(x) for x in c.values()])
        if not es_barrera and not re.search(r'argentin|mercosur', texto, re.I): continue
        fecha = f.get('fecha')
        if not fecha or dt.date.fromisoformat(fecha) < limite: continue
        nid = fecha + '-' + slug(f['nombre'])[:60]
        if nid in vistos: continue
        vistos.add(nid)
        origen = re.split(r'→|↔|–|-(?=\s)', c.get('País', ''))[0].strip()
        origen = origen.split(':')[0].split('(')[0].strip()
        origen = PAISES.get(origen, origen)
        expo = ['Exporta']
        if re.search(r'insumo|importa', c.get('Productos', '') + c.get('Medida', ''), re.I): expo.append('Importa insumos')
        novedades.append({'id': nid, 'fecha_dato': fecha, 'titulo': f['nombre'],
                          'resumen': resumen60(c.get('Medida', ''), c.get('Estado', '')),
                          'tipo': 'medida comercial', 'eje': EJE,
                          'alcance': pais(origen) if origen else ARG,
                          'rubros': rubros_de(c.get('Productos', '') + ' ' + f['nombre']),
                          'subrubros': [], 'exposicion': expo, 'url': f.get('url') or SITIO + '#economia'})
    novedades.sort(key=lambda n: n['fecha_dato'], reverse=True)

    # Agenda: próximos 60 días (decisiones de tasas y elecciones del calendario del sitio).
    agenda, fin = [], hoy.date() + dt.timedelta(days=60)
    for e in d.get('agenda_informe', []):
        f = dt.date.fromisoformat(e['fecha'])
        if hoy.date() <= f <= fin: agenda.append(e)
    meses = {'Ene': 1, 'Feb': 2, 'Mar': 3, 'Abr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Ago': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dic': 12}
    for g in d.get('calendario', {}).get('elecciones', []):
        m = re.match(r'(\w{3})\w* (\d{4})', g.get('mes', ''))
        if not m or m.group(1) not in meses: continue
        for it in g.get('items', []):
            dm = re.match(r'(\d{1,2})/(\d{1,2})', it.get('fecha', ''))
            if not dm: continue
            try: f = dt.date(int(m.group(2)), int(dm.group(2)), int(dm.group(1)))
            except ValueError: continue
            if hoy.date() <= f <= fin:
                agenda.append({'fecha': f.isoformat(), 'evento': f"Elecciones en {it['pais']}: {it.get('tipo', '')}".strip(),
                               'eje': 'Política internacional', 'alcance': pais(it['pais']), 'rubros': [], 'url': SITIO + '#politica'})
    agenda.sort(key=lambda e: e['fecha'])

    out = {'web': 'Monitor Mundial', 'version': '1.0', 'generado': hoy.replace(microsecond=0).isoformat(),
           'indicadores': indicadores, 'novedades': novedades, 'agenda': agenda, 'faltantes': faltantes}
    json.dump(out, open(SALIDA, 'w'), ensure_ascii=False, indent=1)
    print(f'datos-informe.json: {len(indicadores)} indicadores, {len(novedades)} novedades, {len(agenda)} en agenda, {len(faltantes)} faltantes')

if __name__ == '__main__':
    main()
