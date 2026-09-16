"""Genera docs/index.html: landing-galeria de los 17 temas."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.ranking.fechas import fecha_corta
DATA = os.path.join(ROOT, "data")
SITE = os.path.join(ROOT, "docs")

TOP_DATA = json.load(open(os.path.join(DATA, "repos.json"), encoding="utf-8"))
top = TOP_DATA["repos"]
tre = json.load(open(os.path.join(DATA, "trending.json"), encoding="utf-8"))["repos"]
tot_stars = sum(x["stars"] for x in top)
FECHA = fecha_corta(TOP_DATA.get("fecha", ""))
SITEURL = (os.environ.get("SITE_URL") or "").strip().rstrip("/")
UMAMI_URL = (os.environ.get("UMAMI_URL") or "").strip()
UMAMI_ID = (os.environ.get("UMAMI_ID") or "").strip()
UMAMI = ('<script defer src="%s" data-website-id="%s"></script>' % (UMAMI_URL, UMAMI_ID)) if (UMAMI_URL and UMAMI_ID) else ""

def miles(n):
    if n >= 1000000:
        return ("%g millones" % round(n / 1000000, 1)).replace(".", ",")
    if n >= 1000:
        return ("%g mil" % round(n / 1000, 1)).replace(".", ",")
    return str(n)

# archivo, nombre mostrable, layout, fondo, tarjeta, tinta, acento, fuentes
TEMAS = [
    ("01-signal-cards", "Signal", "tarjetas", "#FAFAF7", "#FFFFFF", "#16130E", "#D63A2F", "Archivo + IBM Plex Mono"),
    ("02-midnight-console", "Consola", "tabla", "#0A0E14", "#11161F", "#E6E1D8", "#4ADE80", "Sora + JetBrains Mono"),
    ("04-ledger-table", "Libro", "tabla", "#FBFAF7", "#FFFFFF", "#1F1B16", "#1D4ED8", "Roboto Slab + IBM Plex Mono"),
    ("05-tide-glass", "Marea", "tarjetas", "#0B1B26", "#16283A", "#F2F7FA", "#5EEAD4", "Outfit"),
    ("07-control-tower", "Torre", "dividida", "#F2F4FA", "#FFFFFF", "#141A2B", "#4F46E5", "DM Sans + JetBrains Mono"),
    ("08-atlas-kanban", "Atlas", "kanban", "#F4F7FA", "#FFFFFF", "#10202E", "#0284C7", "Manrope"),
    ("09-phosphor-terminal", "Fósforo", "tabla", "#041008", "#06130B", "#B6FFC9", "#4ADE80", "VT323 + IBM Plex Mono"),
    ("11-gallery-wall", "Galería", "bento", "#141210", "#1E1B17", "#F5EFE4", "#F59E0B", "Sora + Hanken Grotesk"),
    ("14-block-party", "Bloque", "tarjetas", "#FFF3D6", "#FFFFFF", "#000000", "#FF5C00", "Archivo Black + Space Mono"),
    ("15-plum-material", "Pluma", "tarjetas", "#F4EFFA", "#FFFFFF", "#221B2E", "#7C3AED", "Figtree + IBM Plex Mono"),
    ("16-cave-git", "Cueva", "lista", "#0D1117", "#161B22", "#E6EDF3", "#2F81F7", "IBM Plex Mono"),
    ("21-podium", "Podio", "podio", "#101828", "#1A2436", "#F8F3E7", "#FBBF24", "Oswald + Cabin"),
    ("23-night-drive", "Nocturna", "tarjetas", "#08090D", "#101218", "#EDEFF5", "#34D399", "Sora + JetBrains Mono"),
    ("28-abyss", "Abismo", "tabla", "#041E2E", "#07293D", "#E8F6FF", "#22D3EE", "Chakra Petch + IBM Plex Mono"),
    ("29-evergreen", "Perenne", "tarjetas", "#0A1F14", "#10281A", "#E9F5EC", "#4ADE80", "Bitter + Work Sans"),
    ("30-ember", "Brasa", "bento", "#1A0E08", "#241209", "#FBF3E8", "#F97316", "DM Serif Display + Karla"),
    ("trending", "Tendencias", "tarjetas", "#070B14", "#111A2E", "#E8ECF5", "#22D3EE", "Sora + JetBrains Mono"),
]

cards = []
for f, nombre, layout, bg, card, ink, acc, fonts in TEMAS:
    cards.append(
        "<article class='tcard' data-bus='%s %s' style='background:%s;color:%s;border:1px solid %s'>"
        "<div class='sw' style='background:%s'><span style='background:%s'></span></div>"
        "<h3>%s</h3><p class='tl'>%s · %s</p><p class='tf'>%s</p>"
        "<a style='background:%s' href='%s.html'>Abrir tema</a></article>"
        % (nombre.lower(), layout, card, ink, acc, bg, acc, nombre, layout, "claro" if sum(int(bg[i:i+2], 16) for i in (1, 3, 5)) > 384 else "oscuro", fonts, acc, f))

html = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ranking GitHub en español — 500 repos + tendencias, 17 temas</title>
<meta name="description" content="Explorador en español de los 500 repositorios con más estrellas de GitHub y las tendencias del mes. 17 temas visuales, filtros, vista previa y descargas a Excel, CSV, JSON y PDF.">
<meta property="og:title" content="Ranking GitHub en español">
<meta property="og:description" content="500 repos + 200 tendencias, 17 temas, filtros y descargas.">
<meta property="og:type" content="website">
__CANON__
<meta name="twitter:card" content="summary">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
body{background:#070B14;color:#E8ECF5;font-family:'Sora',system-ui,sans-serif;margin:0}
.wrap{max-width:1100px;margin:0 auto;padding:20px}
.hero{padding:36px 0 8px}.hero h1{font-size:clamp(28px,5vw,52px);margin:0;letter-spacing:-.02em}
.hero h1 em{font-style:normal;color:#22D3EE}
.stats{display:flex;gap:12px;flex-wrap:wrap;margin:18px 0}
.stat{background:#111A2E;border:1px solid #2A3550;border-radius:12px;padding:12px 18px}
.stat b{font-size:24px;display:block}.stat span{color:#9AA7C2;font-size:13px}
.bar{position:sticky;top:8px;background:#111A2E;border:1px solid #2A3550;border-radius:12px;padding:10px;display:flex;gap:8px;z-index:5;margin:14px 0}
.bar input{flex:1;background:#0B1222;color:#E8ECF5;border:1px solid #2A3550;border-radius:8px;padding:9px 12px;font:inherit}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
@media(max-width:900px){.grid{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.grid{grid-template-columns:1fr}}
.tcard{border-radius:14px;padding:14px;display:flex;flex-direction:column;gap:6px}
.tcard h3{margin:0;font-size:20px}.tl{margin:0;opacity:.75;font-size:13px}.tf{margin:0;opacity:.6;font-size:12px}
.tcard a{margin-top:8px;text-align:center;color:#070B14;font-weight:700;text-decoration:none;border-radius:9px;padding:10px}
.sw{height:44px;border-radius:9px;display:flex;align-items:end;padding:6px}
.sw span{width:44px;height:10px;border-radius:99px;display:block}
section{margin:26px 0}h2{font-size:24px}
.feat{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.feat div{background:#111A2E;border:1px solid #2A3550;border-radius:12px;padding:14px}
@media(max-width:700px){.feat{grid-template-columns:1fr}}
footer{color:#9AA7C2;font-size:13px;margin:30px 0}
a{color:#22D3EE}:focus-visible{outline:3px solid #22D3EE;outline-offset:2px}
code{background:#111A2E;padding:2px 6px;border-radius:6px}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
</style></head>
<body><div class="wrap">
<header class="hero">
<p style="color:#9AA7C2" class="mono">Datos del __FECHA__ · se actualiza solo cada lunes</p>
<h1>El ranking de GitHub, <em>en español</em> y con 17 caras.</h1>
<p style="color:#9AA7C2">Los 500 repositorios con más estrellas + 200 tendencias del mes. Filtra, previsualiza y descarga. Cada tema es un archivo independiente que funciona con doble clic.</p>
<div class="stats">
<div class="stat"><b>__N500__</b><span>repositorios top</span></div>
<div class="stat"><b>__NTRE__</b><span>tendencias del mes</span></div>
<div class="stat"><b>__STARS__</b><span>estrellas sumadas</span></div>
<div class="stat"><b>17</b><span>temas visuales</span></div>
</div></header>
<div class="bar"><input id="q" placeholder="Filtra temas: terminal, claro, bento..." aria-label="Filtrar temas"></div>
<section><h2>Temas</h2><div class="grid" id="g">__CARDS__</div></section>
<section><h2>Qué sabe hacer</h2><div class="feat">
<div><b>Dos módulos por archivo.</b> Los 500 y Tendencias conviven en cada tema con interruptor propio.</div>
<div><b>Filtros de fecha reales.</b> Día exacto o rangos de 5, 15 y 30 días sobre fecha de creación.</div>
<div><b>Descargas.</b> CSV, Excel (filtrado o completo), JSON y PDF desde el navegador.</div>
<div><b>Datos con pipeline.</b> <code>scripts/</code> va de la API al sitio; un Action lo refresca cada lunes.</div>
</div></section>
<footer>Hecho con la API pública de GitHub · <a href="top500.xlsx">Excel 500</a> · <a href="trending.xlsx">Excel tendencias</a></footer>
</div>
<script>
const q = document.getElementById('q'), cards = [...document.querySelectorAll('.tcard')];
q.addEventListener('input', () => {
  const v = q.value.toLowerCase();
  cards.forEach(c => c.style.display = c.dataset.bus.includes(v) ? '' : 'none');
});
</script>__UMAMI__</body></html>"""

html = html.replace("__N500__", str(len(top))).replace("__NTRE__", str(len(tre)))
html = html.replace("__UMAMI__", UMAMI)
html = html.replace("__FECHA__", FECHA)
html = html.replace("__CANON__", ('<link rel="canonical" href="%s/">' % SITEURL) if SITEURL else "")
html = html.replace("__STARS__", miles(tot_stars) + " estrellas").replace("__CARDS__", "".join(cards))
open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(html)
print("landing ok:", len(html) // 1024, "KB")
