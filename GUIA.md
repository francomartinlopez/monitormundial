# Guía de actualización semanal — Monitor Mundial

Esta guía la sigue Claude cada viernes a la noche. El sitio es estático: `index.html` (estructura y gráficos), `mundo.json` (mapa base, no se toca) y `datos/semana.json` (todos los datos de la semana). **Cada semana se cambia solo `datos/semana.json`**, salvo que haga falta un bloque nuevo.

## Reglas editoriales

- **Qué cubre:** solo lo que pasa fuera de Argentina y cómo afecta a Argentina. La única excepción es la injerencia extranjera dentro de Argentina. Nada de política o hechos internos argentinos.
- **Sin relación** con el proyecto de El Niño en Argentina (alertahidrica / datosargentina).
- **Idioma:** español rioplatense, claro y sin jerga.
- **Corte:** el viernes, al cierre de Wall Street. **Publicación:** el mismo viernes a la noche (la tarea corre a las 21:50, hora argentina). Solo valores actuales; no hay alertas entre semanas.
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
2. **Fechas:** actualizar `corte` (el viernes, AAAA-MM-DD) y `publicado` (el mismo viernes).
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
   - Bloque "Alimentos, cripto y viajes": índices FAO (salen el primer viernes de cada mes), bitcoin, combustible de aviones (IATA/Eurocontrol) y pasajes (IATA). Bloque "Gasto militar" (SIPRI, sale en abril; actualizar si hay anuncios grandes).
   - `crimen`: carteles, mafias y rutas de la droga (México, Andes, Ecuador, Brasil, Paraguay y Triple Frontera, Caribe y Venezuela, Europa, Asia). KPIs: UNODC (sale en junio), ataques de EE.UU. a narcolanchas (Comando Sur) y homicidios en Ecuador. Fuente principal: InSight Crime.
   - Demografía: 16 países (los 13 prioritarios más Nigeria, Pakistán y Etiopía).
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


## Votaciones en la ONU (bloque `onu`)

- Datos en `semana.json` → `onu`: `grupos` (país → grupo regional) y `votos` (lista). Cada votación: `id, titulo, corto, cuerpo` (AG / CS / comisión), `fecha, simbolo, url, resultado, tema` (lista con `"arg"` = tema que importa a Argentina, `"mundo"` = gran tema mundial; puede tener los dos), `porque` (una frase sobre por qué importa) y `votos` (nombre del país en español → `Y` a favor, `N` en contra, `A` abstención, `X` no votó).
- Fuentes: registro de votación de la Biblioteca Digital de la ONU (digitallibrary.un.org, "Voting data") y comunicados de prensa de la ONU (press.un.org). Usar los 193 países en la Asamblea y los 15 miembros en el Consejo. Si algún voto se completa por descarte o por una fuente secundaria, aclararlo en `porque` o en la nota.
- Agregar una votación nueva cuando haya una votación relevante en la semana (en especial si Argentina vota distinto que su bloque habitual o en temas de Malvinas, Medio Oriente, Ucrania, Cuba, Agenda 2030, género o desarme). No borrar las anteriores; dejar como máximo unas 20, quitando las menos relevantes.

## Relación con cada gobierno (mapa 4 y bloque `relaciones`)

- `semana.json` → `relaciones`: lista de `{pais, iso, lider, cat, hecho, url, f}`; `cat` ∈ `aliado, afin, pragmatico, tension, enfrentado`.
- `mapas["4"].paises`: código ISO numérico → color de la categoría (aliado `#2F80ED`, afín `#56C2A6`, pragmático `#8A9AA5`, tensión `#E3BE55`, enfrentado `#F0675F`). Mantener ambos en sincronía.
- Cada país necesita un hecho documentado con fecha y fuente (visita, acuerdo, declaración, incidente diplomático, voto). Sin hecho verificado de los últimos dos años, el país no se colorea.
- Revisar cada semana: cambios de gobierno (la relación es entre gobiernos), insultos o elogios públicos, llamados de embajadores, acuerdos firmados y votos en la ONU. Si cambia la categoría, actualizar el hecho y la fecha.

## Actualizaciones de mitad de semana (elecciones)

Cuando una tarea carga un resultado electoral entre dos cortes semanales, además de la ficha del país, el calendario y los mapas, reescribí la **Lectura de la semana** (`resumen`): el `titular` tiene que nombrar la elección si es relevante para Argentina, y el resultado va en su propio párrafo de `texto` (qué pasó, cifras con fuente y por qué importa a Argentina). Actualizá también `mirar`. No cambies `corte`.

## Sección "Eventos y libertades"

### Mapa de eventos (`semana.json` → `eventos`), se actualiza cada viernes
- Estructura: `{"desde":"AAAA-MM-DD","lista":[{f, cat, geo, pais, iso, lat, lon, r, t, d, fuente, url}]}`.
- `desde`: el día siguiente al corte anterior. Los eventos con `f >= desde` se ven fuertes; los de las tres semanas anteriores, en tono claro. Cada viernes: poné el nuevo `desde`, agregá los eventos de la semana y borrá los de más de 4 semanas.
- `cat`: `excepcion` (emergencia nacional, toque de queda, ley marcial, estado de sitio), `natural` (terremotos de magnitud 6,5 o más o con muertos, tsunamis, erupciones, inundaciones y huracanes graves), `infraestructura` (trenes, barcos, aviones, represas, puentes, plantas nucleares, laboratorios, explosiones industriales con 10 o más muertos o impacto estratégico), `ambiental` (derrames, fugas químicas o radiactivas), `muerte` (muerte natural de figura relevante), `asesinato` (asesinato político), `renuncia` (renuncias y destituciones), `otro` (golpes, apagones masivos, cortes nacionales de internet, ciberataques a infraestructura, disolución del parlamento o juicio político, corralito o default, cierre de fronteras).
- Figuras relevantes: jefes de Estado y de gobierno, ministros, jueces de cortes supremas, jueces y fiscales de casos relevantes (causas contra gobernantes, corrupción a gran escala, repercusión internacional o vínculo con Argentina), presidentes de bancos centrales, jefes militares, líderes de organismos internacionales, de partidos principales y religiosos.
- `geo`: `pais` (pinta todo el país; usa `iso`), `zona` (círculo con `lat`, `lon` y radio `r` en km), `punto` (`lat`, `lon`).
- No van guerras, protestas, brotes ni atentados (tienen sus mapas); sí un asesinato político puntual.
- Fuentes: USGS (sismos), GDACS, ReliefWeb, NASA EONET, NetBlocks (internet) y prensa con fecha verificada.

### Mapas de índices (`datos/indices.json`), se actualizan una vez por año
Cada índice: `{fuente, url, edicion, proxima, cats, paises:{ISO numérico: {cat, v, rk, ...}}}`. Las claves son códigos ISO 3166-1 numéricos de 3 dígitos, como en `mundo.json`. `nombres` tiene el nombre en español de cada país del mapa.
- `regimen`: EIU Democracy Index (democracia plena, democracia no plena, autocracia = régimen híbrido, dictadura = autoritario). Monarquías: `mon` = `absoluta` (cat "monarquía absoluta"), `compartida` (cat "monarquía con poder compartido") o `decorativa` (se pinta según la EIU y `aclara` lo explica). `fallido: true` según el Fragile States Index (se ve rayado).
- `prensa`: RSF (buena, satisfactoria, problemática, difícil, muy grave). Sale entre abril y mayo.
- `economica`: Heritage Foundation (libre, mayormente libre, moderadamente libre, mayormente no libre, reprimida). Sale entre febrero y marzo. Aclarar que Heritage es un centro de estudios conservador.
- `internet`: Freedom House "Freedom on the Net" (`src:"FH"`) y, para los países que no evalúa, V-Dem (`src:"VDem"`, tono claro) con cortes calibrados; el texto del empalme va en `empalme`.
- `pena`: Amnistía Internacional (abolicionista, abolicionista salvo delitos excepcionales, abolicionista en la práctica, la mantiene; `ejecuto:true` y `ej` para los que ejecutaron el último año).
- `visas`: requisitos para pasaporte argentino (sin visa, visa al llegar o electrónica, visa previa, no admitido). Revisar una vez por mes en la actualización semanal del primer viernes del mes.
- `corrupcion`: Índice de Percepción de la Corrupción de Transparencia Internacional, tramos de 20 puntos. Sale en febrero.
Cuando sale una edición nueva, la actualización semanal de esa semana reemplaza el índice completo, cambia `edicion` y `proxima`, y lo menciona en la portada si Argentina cambió de categoría.
