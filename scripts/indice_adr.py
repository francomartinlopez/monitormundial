#!/usr/bin/env python3
"""Índice de ADR argentinos (cálculo propio) a partir de datos/semana.json → adr.acciones.

Promedio simple de cierre / cierre_2025 de 13 acciones, por 100 (base 31/12/2025 = 100).
Escribe valores["indice-adr"] y agrega el punto a series["indice-adr"] (últimas 12 semanas).
Uso: python3 scripts/indice_adr.py
"""
import json, os, sys
TICKERS = ['GGAL', 'YPF', 'PAM', 'BMA', 'BBAR', 'SUPV', 'CEPU', 'TGS', 'TEO', 'EDN', 'CRESY', 'IRS', 'LOMA']
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(RAIZ, 'datos', 'semana.json')
d = json.load(open(P))
A = {a['ticker']: a for a in d['adr']['acciones']}
falta = [t for t in TICKERS if t not in A or not all(A[t].get(k) for k in ('cierre', 'cierre_prev', 'cierre_2025'))]
if falta:
    sys.exit('Faltan cierres de: ' + ', '.join(falta) + ' (no se publica el índice; anotalo en pendientes)')
coma = lambda x: f'{x:.1f}'.replace('.', ',')
hoy = sum(A[t]['cierre'] / A[t]['cierre_2025'] for t in TICKERS) / len(TICKERS) * 100
ant = sum(A[t]['cierre_prev'] / A[t]['cierre_2025'] for t in TICKERS) / len(TICKERS) * 100
corte = d['adr']['corte']
d['valores']['indice-adr'] = {
    'v': round(hoy, 1), 'u': 'base 31/12/2025 = 100', 'dec': 1, 'f': 'cálculo propio sobre cierres de Yahoo Finance y Stock Analysis',
    'url': 'https://stockanalysis.com/stocks/ggal/history/', 'fecha': corte, 'd': round((hoy / ant - 1) * 100, 2), 'dt': 'pct', 'sig': '+',
    'nota': 'Promedio simple de 13 ADR (' + ', '.join(TICKERS) + '), cada uno relativo a su cierre del 31/12/2025. '
            'Viernes anterior: ' + coma(ant) + '. ' + ('Pierde ' if hoy < 100 else 'Gana ') + coma(abs(hoy - 100)) + ' % en el año.'}
s = d.setdefault('series', {}).setdefault('indice-adr', {'labels': [], 'values': [], 'u': 'base 31/12/2025 = 100', 'src': 'cálculo propio'})
lab = corte[8:10] + '/' + corte[5:7]
if lab in s['labels']:
    s['values'][s['labels'].index(lab)] = round(hoy, 1)
else:
    s['labels'].append(lab); s['values'].append(round(hoy, 1))
s['labels'], s['values'] = s['labels'][-12:], s['values'][-12:]
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=1)
print('índice ADR', round(hoy, 1), 'semana anterior', round(ant, 1))
