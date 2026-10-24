# Guía de actualización semanal — Monitor Mundial

Esta guía la sigue Claude cada sábado. El sitio es estático: `index.html` (estructura y gráficos), `mundo.json` (mapa base, no se toca) y `datos/semana.json` (todos los datos de la semana). **Cada semana se cambia solo `datos/semana.json`**, salvo que haga falta un bloque nuevo.

## Reglas editoriales

- **Qué cubre:** solo lo que pasa fuera de Argentina y cómo afecta a Argentina. La única excepción es la injerencia extranjera dentro de Argentina. Nada de política o hechos internos argentinos.
- **Sin relación** con el proyecto de El Niño en Argentina (alertahidrica / datosargentina).
- **Idioma:** español rioplatense, claro y sin jerga.
- **Corte:** el viernes, al cierre de Wall Street. **Publicación:** el sábado. Solo valores actuales; no hay alertas entre semanas.
- **Fuentes:** solo gratuitas. ACLED no se usa.
- **Datos con fuente:** cada dato lleva fuente (`f`), enlace (`url`) y fecha (`fecha`). No se inventa ni se completa de memoria: si no hay fuente, el dato queda en "—" con una nota.
- **Juicios propios:** se marcan como "lectura propia".
- **Sustitutos:** se aclaran en la nota.
  - EMBI → índice de bonos corporativos emergentes de ICE BofA, vía FRED.
  - Contenedor Asia–Sudamérica → índice mundial de Drewry (WCI).
  - Intensidad de conflictos → nivel de 1 a 5 de lectura propia.
- **Cifras sensibles:** muertos, encuestas y resultados se verifican en al menos dos medios.

## Paso a paso

1. **Clonar el repositorio** `francomartinlopez/monitormundial` y leer `datos/semana.json`.
2. **Fechas:** actualizar `corte` (el viernes, AAAA-MM-DD) y `publicado` (el sábado).
3. **Valores** (`valores`): actualizar cada uno con `v`, `d` (variación semanal) y `dt`.
   - `dt`: `"pct"` para %, `"pb"` para puntos básicos, `"pts"` para puntos.
   - `sig`: `"+"` si subir es bueno para Argentina, `"-"` si es malo.
   - Fuentes que funcionan: Investing.com y Brownfield (granos), CurrencyBeacon (monedas), FRED, Trading Economics (vía búsqueda), Pink Sheet del Banco Mundial (fertilizantes y carne; sale a comienzos de mes) y OilPriceAPI (Drewry WCI).
4. **Canasta exportadora** (`series.canasta`):
   - Agregar el cierre del viernes de soja, maíz y trigo de Chicago.
   - Recalcular con base 21/8 = 100: soja 1240,25, trigo 699,75, maíz 508,25 ¢/bu. Pesos: soja 60 %, maíz 25 %, trigo 15 %.
   - Dejar a la vista las últimas 12 semanas.
   - Actualizar el KPI `indice-canasta-exportadora`.
5. **Fichas** (`fichas`): reescribir cada ficha con lo que pasó en la semana. Las que tienen nombres fijos son `bancos`, `pasos`, `sudamerica`, `injerencia-arg`, `influencia-arg` y `demografia`.
   - `influencia-arg`: influencia en Argentina de Estados Unidos, Israel, China, Rusia, Reino Unido y Otros. Cada ficha separa los canales Política, Inteligencia y Económica, y suma la novedad de la semana. El chip indica el peso: Alto, Medio o Bajo.
   - `influyentes`: personas y empresas con influencia en Argentina (Peter Thiel, Palantir, Musk/Starlink, OpenAI, JPMorgan, fondos, XRG, mineras y petroleras). Revisar cada semana si hay novedades y agregar actores nuevos.
   - El KPI `politicos` cuenta los hechos de injerencia política de la semana. En el mapa 14, los colores son: militar rojo, política azul (#5BA4E6), inteligencia violeta y económica ámbar.
   - El mapa 5 (protestas) es mundial y no solo de Sudamérica.
   - `importaciones`: de dónde viene lo que Argentina importa (GNL, urea, fosfatados, potasio, gasoil, soja, autos, celulares). Actualizar con el informe mensual de comercio exterior (ICA) del INDEC y con los riesgos de abastecimiento.
   - Valores semanales nuevos: las bolsas del mundo (S&P 500, Nasdaq, Dow Jones, Euro Stoxx 50, Nikkei, Shanghai, Hang Seng, Ibovespa, FTSE 100, DAX, Kospi y Sensex) y las reservas estratégicas de petróleo (spr-eeuu sale de la EIA todos los miércoles; spr-aie con las liberaciones).
   - `series.deuda` (deuda pública sobre PBI, FMI) se actualiza en abril y octubre. Los KPIs de deuda mundial salen del IIF (trimestral). Las fichas de hechos son `conflictos`, `atentados`, `protestas`, `comercio`, `sanciones`, `ataques`, `ia`, `brotes`, `actores`, `organismos` y `movimientos`.
   - Cada ficha lleva `chip` y `chipc`. Valores de `chipc`: `ok`, `warn` o `crit`.
6. **Gráficos** (`series`):
   - `encuestas`: la próxima elección relevante.
   - `brotes`: casos acumulados.
   - `enso-trim`: IRI, sale a mediados de mes.
   - `intensidad`: los 5 conflictos más intensos de la semana.
   - `pib`: solo cuando el FMI actualiza (abril, julio, octubre y enero).
   - `red`: cuando cambian alianzas.
   - `poblacion`: una vez por año.
7. **Calendario electoral** (`calendario`):
   - Sacar las elecciones ya pasadas y cargar su resultado en la ficha del país.
   - Agregar las nuevas para los próximos 6 meses.
   - `alineado`: `si`, `no` o `incierto` según el favorito sea afín o no al gobierno argentino.
8. **Mapas** (`mapas` "1"–"15"):
   - Colores de países por código ISO numérico.
   - `puntos` con `lat`, `lon`, `c`, `r`, `t` y `lbl`.
   - `lineas` con `de`, `a`, `c`, `dash` y `t`.
   - Mapa 3 (elecciones) y mapa 4 (afinidad): actualizar si hubo elecciones.
9. **Portada:**
   - `resumen`: titular, 2 o 3 párrafos y "qué mirar".
   - `noticias.portada`: las 3 noticias de mayor impacto, con su "por qué importa".
   - `semaforos`: por canal.
   - `vulner`: vulnerabilidades externas.
   - `notas.atlantico`: Malvinas, pesca y Atlántico Sur.
10. **Verificar:**
    - Validar el JSON.
    - Levantar `python3 -m http.server`, abrir el sitio con Playwright y revisar que no haya errores de consola ni "—" nuevos sin nota.
    - Revisar a ojo la portada y 3 bloques al azar.
11. **Publicar:**
    - Hacer commit ("Actualización semanal: corte DD/MM") y push a `main`. GitHub Pages publica solo.
    - Si está disponible, republicar también el artifact "Monitor Mundial" (slug `554a6ca3-822d-46b0-9def-d8e06dd04fdf`) con `publish_files`, enviando `index.html`, `mundo.json` y `datos/semana.json`.
12. **Avisar:** mandar un mail a francomartinlopez@gmail.com con:
    - el titular de la semana;
    - las 3 noticias principales;
    - el enlace al sitio;
    - la lista de datos que quedaron sin fuente.

## Calendario de fuentes que no son semanales

- Pink Sheet del Banco Mundial (fertilizantes, carne): primeros días hábiles del mes.
- NOAA CPC, discusión ENSO: segundo jueves del mes. IRI: alrededor del 19 de cada mes.
- Remesas de México (Banxico): primeros días del mes.
- FMI WEO: abril, julio, octubre y enero.
- ONU WPP: población; revisión cada dos años.
