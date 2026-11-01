#!/usr/bin/env python3
"""Serie semanal de la anomalía de temperatura del Pacífico en la región Niño 3.4.

Arma datos/nino.json para el gráfico de la página Clima: cada año desde 1982 como una línea
que va de enero de ese año a junio del siguiente (así se ve el desarrollo y el pico de cada Niño).
Fuente: NOAA CPC, índice semanal OISST v2.1 (anomalías respecto de 1991–2020), archivo wksst9120.for.
Uso: python3 scripts/nino.py   (cada semana; rehace todo el archivo, tarda segundos)
"""
import json, os, re, datetime as dt, urllib.request
URL = 'https://www.cpc.ncep.noaa.gov/data/indices/wksst9120.for'
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MES = {m: i + 1 for i, m in enumerate(['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'])}

def main():
    txt = urllib.request.urlopen(URL, timeout=60).read().decode()
    serie = []
    for l in txt.splitlines():
        m = re.match(r'\s*(\d{2})([A-Z]{3})(\d{4})\s+(.*)', l)
        if not m: continue
        nums = re.findall(r'-?\d+\.\d', m.group(4))
        if len(nums) < 8: continue
        serie.append((dt.date(int(m.group(3)), MES[m.group(2)], int(m.group(1))), float(nums[5])))
    anios = {}
    for y in range(1982, serie[-1][0].year + 1):
        ini, fin = dt.date(y, 1, 1), dt.date(y + 1, 6, 30)
        pts = [[(d - ini).days, a] for d, a in serie if ini <= d <= fin]
        if not pts: continue
        pico = max(((d, a) for d, a in serie if dt.date(y, 9, 1) <= d <= dt.date(y + 1, 2, 28)), key=lambda x: x[1], default=None)
        anios[str(y)] = {'p': pts, 'pico': [pico[0].isoformat(), pico[1]] if pico else None}
    out = {'fuente': 'NOAA CPC, Niño 3.4 semanal (OISST v2.1, anomalía respecto de 1991–2020)', 'url': URL,
           'ultimo': [serie[-1][0].isoformat(), serie[-1][1]], 'anios': anios}
    json.dump(out, open(os.path.join(RAIZ, 'datos', 'nino.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    print('último', out['ultimo'])

if __name__ == '__main__': main()
