<p align="center">
  <h1 align="center">📊 Pulso GitHub</h1>
  <p align="center"><strong>El ranking de GitHub, en español y con 17 caras.</strong><br>500 repos con más estrellas + 200 tendencias. Filtra, previsualiza, descarga y explóralo en 3D.</p>
  <p align="center">
    <a href="https://github.com/Marusan94/pulso-github/actions/workflows/refresh.yml"><img src="https://github.com/Marusan94/pulso-github/actions/workflows/refresh.yml/badge.svg" alt="refresh semanal"></a>
    <img src="https://img.shields.io/badge/python-3.11-blue" alt="python 3.11">
    <img src="https://img.shields.io/badge/espa%C3%B1ol-100%25-red" alt="español">
    <img src="https://img.shields.io/badge/datos-lunes_06%3A00_UTC-green" alt="refresco semanal">
    <img src="https://img.shields.io/badge/licencia-MIT-yellow" alt="MIT">
  </p>
</p>

| Inicio (tema Consola) | Analytics | Noticias |
|---|---|---|
| ![Inicio](assets/inicio-consola.png) | ![Analytics](assets/analytics.png) | ![Noticias](assets/noticias.png) |

## ✨ Qué hace

- 🔍 **Dos módulos**: Los 500 + Tendencias (30 días), con buscador, categoría, licencia, fecha exacta o rangos y 4 ordenamientos.
- 📈 **Dinámica real**: flechas ▲▼ de puestos, rachas 🔥, Top subidas/caídas y vista "En el tiempo" desde el segundo corte.
- 📊 **Analytics**: curva logarítmica con etiquetas, radar por categoría, líderes de crecimiento (CSV), histograma y serie por repo al clic.
- 📰 **Noticias** generadas de los datos: hitos, recién llegados y rachas.
- 🌌 **Galaxia 3D** (`docs/galaxia.html`): los 500 + 200 tendencias como constelaciones por categoría, tamaño por estrellas y color por lenguaje. Clic para ficha y vuelo de cámara, hover con etiqueta, conexiones entre similares, buscador y filtros. Cero backend: HTML estático con datos embebidos.
- 🇪🇸 **Descripciones en español claro**: traducción sintética de lo que hace cada repo + ficha mínima, sin relleno genérico.
- 🎨 **17 temas** que te siguen a todas las vistas (`?tema=`), con contraste validado. La entrada abre el tema Consola.
- ⬇️ **Descargas**: CSV, Excel, JSON y PDF. **Mis elegidos** ☆ guardados en tu navegador.
- 🔒 **Privacidad**: cero cookies en local; analytics open source (Umami) solo en producción.

## 🚀 Uso en local

```bash
# Opción 1: doble clic en cualquier HTML de docs/ (galaxia.html pide internet solo por el CDN de Three.js)
# Opción 2 (recomendada): servidor local
cd docs && python -m http.server 8901
# o doble clic en ver.bat → http://localhost:8901/02-midnight-console.html
```

## 🔄 Cómo se actualiza solo

```mermaid
flowchart LR
    API[GitHub Search API] --> FETCH[fetch_*]
    FETCH --> DESC[describe + taxonomía]
    DESC --> SNAP[snapshot semanal]
    SNAP --> BUILD[build_site + build_paginas + build_galaxia]
    BUILD --> CHECK[verify + pytest]
    CHECK --> PUSH[commit + push]
    PUSH --> DEPLOY[redespliegue solo]
```

Cada lunes 06:00 UTC (o manual en Actions → Run workflow). Fechas, ventanas y textos de corte se derivan de los datos: nada hardcodeado. Con `GITHUB_TOKEN` la API va autenticada.

## 🗂️ Estructura

```
├── data/               # repos.json (500) + trending.json (200) + history/
├── docs/               # sitio publicable (17 temas + analytics + noticias + galaxia + xlsx)
├── src/ranking/        # lógica compartida: taxonomia, historial, fechas
├── scripts/            # fetch → describe → snapshot → excel → builds → verify (incluye build_galaxia.py)
├── tests/              # 8 E2E en Chromium real (Playwright)
└── .github/workflows/refresh.yml
```

## ⚙️ Variables de entorno (opcionales)

| Variable | Dónde | Efecto |
|---|---|---|
| `GITHUB_TOKEN` | Actions (automático) | API autenticada, sin rate-limits |
| `SITE_URL` | Actions vars / proveedor | sitemap, canonical y OG con tu dominio |
| `UMAMI_URL` + `UMAMI_ID` | Actions secrets/vars | tracker sin cookies solo en producción |

Sin ellas todo funciona igual, sin tracker ni canonicals.

## 🧪 Calidad

```bash
pip install -r requirements.txt
pip install pytest playwright && python -m playwright install chromium
python scripts/verify.py   # datos + JS (node) + tracker + contraste WCAG
python -m pytest tests -q  # 8 E2E en Chromium
```

Metodología, sesgos y licencia de datos: [`docs/como-esta-hecho.html`](docs/como-esta-hecho.html).

## 📄 Licencia

MIT. Datos: API pública de GitHub (corte incluido en cada archivo); descripciones y taxonomía, propias.
