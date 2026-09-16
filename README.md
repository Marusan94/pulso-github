# Pulso GitHub — ranking en español

Explorador en español de los **500 repositorios con más estrellas** de GitHub más un módulo de **tendencias de los últimos 30 días** (200 repos). 17 temas visuales independientes, páginas de Analytics y Noticias, y todo funciona con doble clic, sin servidor.

## Verlo en local

```bash
# Opción 1: doble clic en cualquier HTML de docs/
# Opción 2: servidor local (recomendado: activa todas las funciones)
cd docs && python -m http.server 8901
# o doble clic en ver.bat → http://localhost:8901/29-evergreen.html
```

Cada archivo es autónomo: trae ambas bases de datos embebidas (~700 registros). Con `file://` todo funciona salvo el analytics externo (solo producción).

## Publicar (Vercel o Netlify)

1. Sube el repo a GitHub e importa el proyecto (Root Directory: `docs`).
2. Define tu dominio y ponlo en la variable `SITE_URL` del proveedor o de Actions (se usa para sitemap, canonical y OG). Sin ella se publica igual, sin esas etiquetas.
3. **Analytics (opcional, solo producción)**: crea un sitio en [Umami](https://umami.is) y define `UMAMI_URL` (URL de tu instancia + `/script.js`) y `UMAMI_ID`. Sin estas variables el build no incluye ningún tracker: cero cookies, cero banner.
4. Cada push a `main` redespliega solo.

> Atajo en Windows: edita `$RepoUrl` en `publicar.ps1` y ejecútalo; hace push, deploy y variables paso a paso.

## Actualización automática

El workflow `.github/workflows/refresh.yml` corre **cada lunes 06:00 UTC** (o manual desde Actions → Run workflow):

`fetch_top` → `fetch_trending` → `describe` → `snapshot` → `export_excel` → `build_site` → `build_paginas` → `gen_landing` → `gen_sitemap` → `verify` → `pytest` → commit + push.

- Las fechas (`fecha`, ventana de 30 días, textos de corte) se derivan de los datos: nada hardcodeado.
- Con `GITHUB_TOKEN` (el de Actions vale) la API va autenticada; en anónimo aguanta con pausas (~10 req/min en Search API).
- `snapshot.py` archiva cada corte en `data/history/` (base de rachas, flechas ▲▼ y la vista "En el tiempo").

## Qué incluye

- **Módulo Los 500 / Tendencias**: buscador, categoría, licencia (MIT/permisivas/copyleft), "solo vivos", "sin awesome-lists", fecha exacta o rangos, 4 ordenamientos (incluye "mayor subida").
- **Dinámica de puestos**: flechas ▲▼, "nuevo en el ranking", tiras Top subidas/caídas/nuevos y rachas 🔥 desde el segundo corte.
- **Analytics**: curva logarítmica con etiquetas y selector Top 30/50/100/200/Todos, vista "En el tiempo", radar por categoría, líderes de crecimiento (CSV), histograma y serie por repo al clic.
- **Noticias**: hitos, recién llegados y rachas generados de los datos.
- **17 temas** que persisten en todas las vistas (`?tema=`), con contraste validado automáticamente.
- **Descargas**: CSV, Excel (filtrado o completo), JSON y PDF; **Mis elegidos** (☆) guardados en el navegador.
- **Privacidad**: sin cookies ni rastreo en local; Umami sin cookies solo en producción.

## Estructura

```
github-ranking/
├── data/                  # repos.json (500) y trending.json (200) + history/
├── docs/                  # sitio publicable (17 temas + analytics + noticias + xlsx)
├── src/ranking/           # lógica compartida: taxonomia, historial, fechas
├── scripts/
│   ├── fetch_top.py / fetch_trending.py  # GitHub Search API (fecha real, token)
│   ├── describe.py        # descripciones en español + categoría/tipo
│   ├── snapshot.py        # archiva el corte en data/history/
│   ├── export_excel.py    # top500.xlsx y trending.xlsx
│   ├── build_site.py      # genera los 17 HTML (+OG/canonical/Umami si hay env)
│   ├── build_paginas.py   # genera analiticas.html y noticias.html
│   ├── gen_landing.py     # genera index.html (portada)
│   ├── gen_sitemap.py     # sitemap.xml (usa SITE_URL si existe)
│   └── verify.py          # JS con node + datos + tracker + contraste
├── tests/test_e2e.py      # 8 tests en Chromium real (Playwright)
└── .github/workflows/refresh.yml  # refresco semanal con gates
```

## Uso

```bash
pip install -r requirements.txt
pip install pytest playwright && python -m playwright install chromium  # solo tests
python scripts/fetch_top.py       # API real; escribe data/repos.json con fecha de hoy
python scripts/fetch_trending.py
python scripts/describe.py
python scripts/snapshot.py
python scripts/export_excel.py
python scripts/build_site.py
python scripts/build_paginas.py
python scripts/gen_landing.py
python scripts/gen_sitemap.py
python scripts/verify.py          # 0 fallos: datos + JS + tracker + contraste
python -m pytest tests -q         # 8 E2E en Chromium
```

## Stack

Python (stdlib + openpyxl) para datos · HTML/CSS/SVG vainilla + SheetJS · Sin build, sin dependencias en el sitio · Umami (solo prod) · CI en GitHub Actions.

## Licencia

MIT. Datos: API pública de GitHub (corte incluido en cada archivo); descripciones en español y taxonomía, propias.
