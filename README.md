# Ranking interactivo de GitHub

Explorador en español de los **500 repositorios con más estrellas** de GitHub más un módulo de **tendencias del último mes** (200 repos). 17 temas visuales independientes, todo funciona con doble clic, sin servidor.

## Demo

Publica la carpeta `docs/` con GitHub Pages y abre cualquiera de los 17 HTML. Cada archivo es autónomo: trae ambas bases de datos embebidas (~700 registros).

## Publicar con dominio propio (recomendado: Vercel)

¿Netlify o Vercel? Ambos sirven para este sitio estático, pero **Vercel** gana aquí: deploys de vista previa por cada cambio (muestran proceso profesional), SSL y dominio gratis, y redespliegue automático con cada push. El `netlify.toml` queda como alternativa.

1. Sube el repo a GitHub y entra a [vercel.com](https://vercel.com) → Add New → Project → importa el repo.
2. En **Root Directory** escribe `docs` (el sitio vive ahí) → Deploy.
3. Compra o usa tu dominio (ej: en Cloudflare, Namecheap) y en Vercel → Settings → Domains → añade `turanking.dev`.
4. Apunta el DNS: registro `A` a `76.76.21.21` o `CNAME` a `cname.vercel-dns.com` (Vercel te dice el exacto). SSL se emite solo.
5. Cambia `TU-DOMINIO` por tu dominio en `docs/robots.txt`, regenera el sitemap (`python scripts/gen_sitemap.py` con tu dominio en `BASE`) y haz push.

## Actualización automática

El workflow `.github/workflows/refresh.yml` corre **cada lunes 06:00 UTC**: trae datos frescos, regenera Excel y los 17 HTML, verifica y hace push. Vercel/Netlify detectan el push y republican solos. Nada manual. También puedes lanzarlo a mano desde Actions → Run workflow.

## Qué incluye

- **Módulo Los 500**: buscador, filtro por categoría, orden por estrellas/bifurcaciones, paginado y vista previa de cada repo.
- **Módulo Tendencias**: filtro por día exacto o rangos (últimos 5 / 15 días / mes), orden por novedad y sello de antigüedad.
- **Descargas**: CSV, Excel (filtrado o completo), JSON y PDF desde cada página.
- **Mis elegidos**: marca con ☆ los repos que te gusten mientras exploras (se guardan en el navegador), filtra la vista a solo ellos y descárgalos aparte en Excel, PDF o CSV.
- **17 temas**: paletas y tipografías distintas (terminal, neobrutalista, bento, kanban, podio...), español total y descripciones ampliadas.
- **Pipeline reproducible**: pasa de la API a los datos y al sitio con 5 scripts.

## Estructura

```
github-ranking/
├── data/               # repos.json (500) y trending.json (200), generados
├── docs/               # sitio publicable (17 HTML + 2 XLSX con hipervínculos)
├── scripts/
│   ├── fetch_top.py       # Top 500 por estrellas (GitHub Search API)
│   ├── fetch_trending.py  # Creados en los últimos 30 días
│   ├── describe.py        # Descripciones en español + categoría/tipo
│   ├── export_excel.py    # top500.xlsx y trending.xlsx
│   ├── build_site.py      # Genera los 17 HTML
│   └── verify.py          # Valida JS con node y datos embebidos
└── .github/workflows/refresh.yml  # refresco semanal automático
```

## Uso

```bash
pip install -r requirements.txt
python scripts/fetch_top.py       # respeta el límite de la API (pausas incluidas)
python scripts/fetch_trending.py
python scripts/describe.py
python scripts/export_excel.py
python scripts/build_site.py
```

Sin token la Search API permite ~10 peticiones/minuto; los scripts ya incluyen las pausas.

## Stack

Python (stdlib + openpyxl) para datos · HTML/CSS/JS vainilla + SheetJS para exports · Sin build, sin dependencias en el sitio.

## Licencia

MIT. Datos: API pública de GitHub (corte incluido en cada archivo).
