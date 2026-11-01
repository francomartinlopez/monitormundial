#!/usr/bin/env python3
"""Serie diaria del viento del vórtice polar (viento zonal medio a 10 hPa y 60° N).

Arma datos/vortice.json para el gráfico de la página Clima:
- Historia: reanálisis NCEP/NCAR R1 (NOAA PSL), promedio diario, temporadas desde 1979/80.
- Temporada en curso: análisis del modelo GFS (NOAA NCEI), promedio de las 4 corridas del día
  (00, 06, 12 y 18 UTC), bajando solo el campo UGRD a 10 hPa con pedidos por rango de bytes.

Uso:
  python3 scripts/vortice.py historia            # una vez (o para rehacer la climatología)
  python3 scripts/vortice.py actualizar --hasta AAAA-MM-DD   # cada semana, con la fecha de corte
  python3 scripts/vortice.py actualizar --hasta 2026-06-30 --temporada 2025/26   # completar huecos de una temporada pasada
Requiere: numpy y eccodes (pip install --break-system-packages eccodes).
"""
import json, sys, os, re, datetime as dt, urllib.request, concurrent.futures as cf
import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, 'datos', 'vortice.json')
PSL = 'https://psl.noaa.gov/thredds/dodsC/Datasets/ncep.reanalysis/Dailies/pressure/uwnd.{y}.nc.ascii?uwnd[0:1:{n}][16][12][0:1:143]'
PSL_DDS = 'https://psl.noaa.gov/thredds/dodsC/Datasets/ncep.reanalysis/Dailies/pressure/uwnd.{y}.nc.dds'
NCEI = 'https://www.ncei.noaa.gov/thredds/fileServer/model-gfs-g4-anl-files/{ym}/{ymd}/gfs_4_{ymd}_{hh}00_000.grb2'

def get(url, rango=None, intentos=4):
    for i in range(intentos):
        try:
            req = urllib.request.Request(url, headers={'Range': f'bytes={rango[0]}-{rango[1]}'} if rango else {})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception as e:
            if i == intentos - 1: raise
    return None

def dia_temporada(d):
    """Índice 0..364 desde el 1 de julio; el 29 de febrero se junta con el 28."""
    ini = dt.date(d.year if d.month >= 7 else d.year - 1, 7, 1)
    n = (d - ini).days
    bis = dt.date(ini.year + 1, 3, 1) - dt.date(ini.year + 1, 2, 28) == dt.timedelta(days=2)
    if bis and d >= dt.date(ini.year + 1, 2, 29): n -= 1
    return min(n, 364)

def temporada(d):
    a = d.year if d.month >= 7 else d.year - 1
    return f'{a}/{str(a + 1)[2:]}'

def historia():
    hoy = dt.date.today()
    diario = {}
    for y in range(1979, hoy.year + 1):
        dds = get(PSL_DDS.format(y=y)).decode()
        nt = int(re.search(r'time = (\d+)', dds).group(1))
        txt = get(PSL.format(y=y, n=nt - 1)).decode()
        filas = [l for l in txt.splitlines() if l.startswith('[')]
        for k, l in enumerate(filas):
            vals = [float(x) for x in l.split(',')[1:]]
            d = dt.date(y, 1, 1) + dt.timedelta(days=k)
            diario[d] = float(np.mean(vals))
        print(y, nt, file=sys.stderr)
    tem = {}
    for d, u in diario.items():
        tem.setdefault(temporada(d), [None] * 365)
        i = dia_temporada(d)
        tem[temporada(d)][i] = u if tem[temporada(d)][i] is None else (tem[temporada(d)][i] + u) / 2
    completas = [t for t, v in tem.items() if all(x is not None for x in v)]
    M = np.array([tem[t] for t in completas])
    pct = {k: np.percentile(M, p, axis=0) for k, p in [('p10', 10), ('p30', 30), ('p70', 70), ('p90', 90)]}
    out = cargar()
    out.update({
        'clima': {'desde': completas[0], 'hasta': completas[-1], 'n': len(completas),
                  'min': r1(M.min(0)), 'p10': r1(pct['p10']), 'p30': r1(pct['p30']), 'media': r1(M.mean(0)),
                  'p70': r1(pct['p70']), 'p90': r1(pct['p90']), 'max': r1(M.max(0))},
        'temporadas': {t: r1(v) for t, v in sorted(tem.items()) if t != temporada(hoy)},
    })
    guardar(out)

def r1(a): return [None if x is None else round(float(x), 1) for x in a]

def u60_gfs(d, hh):
    ym, ymd = d.strftime('%Y%m'), d.strftime('%Y%m%d')
    url = NCEI.format(ym=ym, ymd=ymd, hh=hh)
    inv = get(url + '.inv').decode().splitlines()
    for k, l in enumerate(inv):
        if ':UGRD:10 mb:' in l:
            a = int(l.split(':')[1]); b = int(inv[k + 1].split(':')[1]) - 1
            break
    else: raise RuntimeError('sin UGRD 10 mb en ' + url)
    import eccodes
    g = eccodes.codes_new_from_message(get(url, (a, b)))
    ni, nj = eccodes.codes_get(g, 'Ni'), eccodes.codes_get(g, 'Nj')
    la0, dj = eccodes.codes_get(g, 'latitudeOfFirstGridPointInDegrees'), eccodes.codes_get(g, 'jDirectionIncrementInDegrees')
    v = eccodes.codes_get_values(g).reshape(nj, ni)
    eccodes.codes_release(g)
    return float(v[int(round((la0 - 60) / dj))].mean())

def actualizar(hasta, t=None):
    out = cargar()
    if t:
        # Completar huecos de una temporada pasada (por ejemplo 2025/26, que el reanálisis R1 cubre solo hasta marzo de 2026).
        vals = out['temporadas'][t]
        ini = dt.date(int(t[:4]), 7, 1)
        dias = [ini + dt.timedelta(days=k) for k in range(366) if ini + dt.timedelta(days=k) < dt.date(int(t[:4]) + 1, 7, 1)]
        faltan = [d for d in dias if vals[dia_temporada(d)] is None and d <= hasta]
        def uno(d):
            v = []
            for hh in ('00', '06', '12', '18'):
                try: v.append(u60_gfs(d, hh))
                except Exception as e: print('falla', d, hh, e, file=sys.stderr)
            return d, (sum(v) / len(v) if len(v) >= (4 if (hasta - d).days < 7 else 2) else None)
        with cf.ThreadPoolExecutor(8) as ex:
            for d, u in ex.map(uno, faltan):
                if u is not None: vals[dia_temporada(d)] = round(u, 1)
        out['temporadas'][t] = vals
        guardar(out); print(t, 'completa:', sum(x is not None for x in vals), 'días'); return
    t = temporada(hasta)
    act = out.get('actual') if out.get('actual', {}).get('temporada') == t else {'temporada': t, 'valores': [None] * 365}
    if out.get('actual') and out['actual'].get('temporada') != t:
        out.setdefault('temporadas', {})[out['actual']['temporada']] = out['actual']['valores']
    ini = dt.date(int(t[:4]), 7, 1)
    dias = [ini + dt.timedelta(days=k) for k in range((hasta - ini).days + 1)]
    faltan = [d for d in dias if act['valores'][dia_temporada(d)] is None]
    def uno(d):
        vals = []
        for hh in ('00', '06', '12', '18'):
            try: vals.append(u60_gfs(d, hh))
            except Exception as e: print('falla', d, hh, e, file=sys.stderr)
        # Un día reciente se guarda solo si están las 4 corridas (si falta alguna, se completa la semana próxima);
        # si ya pasó una semana y NOAA sigue sin alguna corrida, alcanza con 2.
        return d, (sum(vals) / len(vals) if len(vals) >= (4 if (hasta - d).days < 7 else 2) else None)
    with cf.ThreadPoolExecutor(8) as ex:
        for d, u in ex.map(uno, faltan):
            if u is not None: act['valores'][dia_temporada(d)] = round(u, 1)
    ult = max((d for d in dias if act['valores'][dia_temporada(d)] is not None), default=None)
    act['ultimo'] = ult.isoformat() if ult else None
    act['fuente'] = 'NOAA NCEI, análisis del modelo GFS (promedio de 00, 06, 12 y 18 UTC)'
    out['actual'] = act
    guardar(out)
    print('último dato', act['ultimo'], 'valor', act['valores'][dia_temporada(ult)] if ult else None)

def cargar():
    try: return json.load(open(SALIDA))
    except FileNotFoundError: return {}

def guardar(o):
    o['unidad'] = 'm/s'
    o['historia_fuente'] = 'NOAA PSL, reanálisis NCEP/NCAR R1 (promedio diario)'
    json.dump(o, open(SALIDA, 'w'), ensure_ascii=False, separators=(',', ':'))

if __name__ == '__main__':
    if sys.argv[1] == 'historia': historia()
    elif sys.argv[1] == 'actualizar':
        h = dt.date.fromisoformat(sys.argv[sys.argv.index('--hasta') + 1]) if '--hasta' in sys.argv else dt.date.today() - dt.timedelta(days=2)
        actualizar(h, sys.argv[sys.argv.index('--temporada') + 1] if '--temporada' in sys.argv else None)
