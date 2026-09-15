"""Genera analiticas.html y noticias.html (autonomas, datos embebidos)."""
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SITE = os.path.join(ROOT, "docs")
TOP_DATA = json.load(open(os.path.join(DATA, "repos.json"), encoding="utf-8"))
TRE_DATA = json.load(open(os.path.join(DATA, "trending.json"), encoding="utf-8"))
TOP = json.dumps(TOP_DATA["repos"], ensure_ascii=False)
TRE = json.dumps(TRE_DATA["repos"], ensure_ascii=False)


def deltas(kind, current):
    snaps = sorted(glob.glob(os.path.join(DATA, "history", "*-" + kind + ".json")))
    prevs = [s for s in snaps if os.path.basename(s)[:10] < current.get("fecha", "")]
    if not prevs:
        return {}, ""
    prev = json.load(open(prevs[-1], encoding="utf-8"))
    old = {r["n"]: r["s"] for r in prev["repos"]}
    return {x["full_name"]: x["stars"] - old.get(x["full_name"], x["stars"]) for x in current["repos"]}, prev["fecha"]


DELTAS = json.dumps({"500": deltas("top", TOP_DATA)[0], "tre": deltas("tre", TRE_DATA)[0]}, ensure_ascii=False)
CORTE = deltas("top", TOP_DATA)[1]

BASE = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ — Ranking GitHub</title>
<meta name="description" content="__DESC__">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link href="https://fonts.googleapis.com/css2?family=Bitter:wght@400;700;800&family=Work+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
body{background:#0A1F14;color:#E9F5EC;font-family:'Work Sans',system-ui,sans-serif;margin:0}
h1,h2,h3{font-family:'Bitter',serif}
.wrap{max-width:1000px;margin:0 auto;padding:16px}
nav.tabs{display:flex;gap:8px;margin-bottom:6px;flex-wrap:wrap}
nav.tabs a{border:1px solid #4ADE80;color:#4ADE80;border-radius:999px;padding:8px 16px;text-decoration:none;font-weight:700}
nav.tabs a.on{background:#4ADE80;color:#05281A}
.mut{color:#8FB69C}
.card{background:#10281A;border:1px solid #1E4A30;border-radius:12px;padding:14px;margin-bottom:12px}
.seg{display:flex;background:#10281A;border:1px solid #1E4A30;border-radius:12px;padding:4px;gap:4px;margin:12px 0}
.seg button{flex:1;background:transparent;border:0;color:#8FB69C;padding:10px;border-radius:8px;cursor:pointer;font-weight:700;font-family:inherit}
.seg button.on{background:#4ADE80;color:#05281A}
.fila{display:grid;grid-template-columns:170px 1fr 90px;gap:8px;align-items:center;margin:6px 0;font-size:14px}
.barra{height:14px;background:#0A1F14;border-radius:99px;overflow:hidden;border:1px solid #1E4A30}
.barra i{display:block;height:100%;background:#4ADE80}
.num{text-align:right;font-variant-numeric:tabular-nums}
a{color:#4ADE80}
.stats{display:flex;gap:10px;flex-wrap:wrap;margin:12px 0}
.stat{background:#10281A;border:1px solid #1E4A30;border-radius:12px;padding:10px 16px}
.stat b{font-size:22px;display:block}
.not{border-left:4px solid #4ADE80;padding:8px 12px;margin-bottom:10px;background:#10281A;border-radius:0 12px 12px 0}
.not small{color:#8FB69C}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:760px){.grid2{grid-template-columns:1fr}.fila{grid-template-columns:120px 1fr 70px}}
:focus-visible{outline:3px solid #4ADE80;outline-offset:2px}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
@media print{.seg,nav{display:none}body{background:#fff;color:#000}.card{border-color:#000}}
</style></head>
<body><div class="wrap">
<nav class="tabs noprint"><a href="analiticas.html" id="t-ana">◔ Analytics</a><a href="noticias.html" id="t-not">📰 Noticias</a><a href="29-evergreen.html">◐ Temas</a></nav>
__BODY__
</div>
<script>
const DB500 = __DB500__;
const DBTRE = __DBTRE__;
const DELTAS = __DELTAS__;
const CORTE = "__CORTE__";
const HOY = '2026-09-14';
const PERMISIVAS = ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "CC0-1.0"];
let module = new URLSearchParams(location.search).get('mod') === 'tre' ? 'tre' : "__MODULE__";
function DB(){ return module === '500' ? DB500 : DBTRE; }
function fmt(n){ if (n >= 1000000) return (n/1000000).toFixed(1).replace('.', ',').replace(',0', '') + ' millones'; return n >= 1000 ? (n/1000).toFixed(n >= 100000 ? 0 : 1).replace(/\\.0$/,'') + ' mil' : '' + n; }
function daysOld(iso){ return Math.round((new Date(HOY) - new Date(iso)) / 86400000); }
function age(iso){ const d = daysOld(iso); return d <= 0 ? 'hoy' : d === 1 ? 'ayer' : 'hace ' + d + ' días'; }
function vivo(x){ return !x.archived && (new Date(HOY) - new Date(x.pushed_at || x.created_at || HOY)) / 2592000000 <= 12; }
function setModule(m){
  module = m; page = 0;
  document.getElementById('m500').classList.toggle('on', m === '500');
  document.getElementById('mtre').classList.toggle('on', m === 'tre');
  render();
}
document.getElementById('m500').onclick = () => setModule('500');
document.getElementById('mtre').onclick = () => setModule('tre');
__PAGEJS__
setModule(module);
</script></body></html>"""

ANA_BODY = """
<p class="mut">700 registros incluidos · corte 14 sep 2026</p>
<h1>Analytics</h1>
<div class="seg" role="group" aria-label="Módulo"><button id="m500" class="on">Los 500</button><button id="mtre">Tendencias</button></div>
<div class="stats" id="stats"></div>
<div class="grid2">
<div class="card"><h3>Por categoría</h3><div id="cats"></div></div>
<div class="card"><h3>Lenguajes top</h3><div id="langs"></div></div>
</div>
<div class="grid2">
<div class="card"><h3>Licencias</h3><div id="lics"></div></div>
<div class="card"><h3>🔥 Top movidas</h3><div id="mov"></div></div>
</div>
"""

ANA_JS = """
let page = 0;
function fila(label, val, max){
  const pct = max ? Math.round(val / max * 100) : 0;
  return `<div class="fila"><span>${label}</span><div class="barra"><i style="width:${pct}%"></i></div><span class="num">${val}</span></div>`;
}
function render(){
  const D = DB(), dm = DELTAS[module] || {};
  const totStars = D.reduce((a, x) => a + x.stars, 0);
  const perm = D.filter(x => PERMISIVAS.includes(x.license)).length;
  const vivos = D.filter(vivo).length;
  document.getElementById('stats').innerHTML =
    `<div class="stat"><b>${D.length}</b>repositorios</div>` +
    `<div class="stat"><b>${fmt(totStars)}</b>estrellas</div>` +
    `<div class="stat"><b>${Math.round(perm / D.length * 100)}%</b>licencia permisiva</div>` +
    `<div class="stat"><b>${Math.round(vivos / D.length * 100)}%</b>vivos</div>`;
  const cats = {};
  D.forEach(x => cats[x.categoria] = (cats[x.categoria] || 0) + 1);
  const ck = Object.keys(cats).sort((a, b) => cats[b] - cats[a]), cmax = cats[ck[0]] || 1;
  document.getElementById('cats').innerHTML = ck.map(k => fila(k, cats[k], cmax)).join('');
  const langs = {};
  D.forEach(x => langs[x.language] = (langs[x.language] || 0) + 1);
  const lk = Object.keys(langs).sort((a, b) => langs[b] - langs[a]).slice(0, 8), lmax = langs[lk[0]] || 1;
  document.getElementById('langs').innerHTML = lk.map(k => fila(k, langs[k], lmax)).join('');
  const copy = D.filter(x => /GPL|AGPL|LGPL/i.test(x.license || '')).length;
  document.getElementById('lics').innerHTML =
    fila('Permisivas', perm, D.length) + fila('Copyleft', copy, D.length) + fila('Otras / sin dato', D.length - perm - copy, D.length);
  const mov = D.filter(x => (dm[x.full_name] || 0) > 0).sort((a, b) => dm[b.full_name] - dm[a.full_name]).slice(0, 5);
  document.getElementById('mov').innerHTML = mov.length
    ? mov.map(x => `<div class="fila"><span><a href="${x.url}" target="_blank" rel="noopener">${x.full_name}</a></span><div class="barra"><i style="width:${Math.round(dm[x.full_name] / dm[mov[0].full_name] * 100)}%"></i></div><span class="num">+${fmt(dm[x.full_name])}</span></div>`).join('')
    : '<p class="mut">Sin movimientos aún: aparecen desde el segundo corte semanal.</p>';
}
"""

NOT_BODY = """
<p class="mut">Titulares generados de tus datos · corte 14 sep 2026</p>
<h1>Noticias</h1>
<div class="seg" role="group" aria-label="Módulo"><button id="m500" class="on">Los 500</button><button id="mtre">Tendencias</button></div>
<div id="feed"></div>
"""

NOT_JS = """
let page = 0;
function item(emoji, titulo, det, x){
  return `<div class="not"><div>${emoji} <a href="${x.url}" target="_blank" rel="noopener"><strong>${x.full_name}</strong></a> — ${titulo}</div><small>${det} · ${x.language} · ${x.categoria} · ${x.license}</small></div>`;
}
function render(){
  const D = DB(), dm = DELTAS[module] || {};
  let html = '';
  if (module === 'tre'){
    const nuevos = D.slice().sort((a, b) => (b.created_at || '').localeCompare(a.created_at || '')).slice(0, 10);
    html += '<h2>🆕 Recién llegados</h2>' + nuevos.map(x => item('🆕', `${fmt(x.stars)} estrellas, ${age(x.created_at)}`, 'Creado el ' + x.created_at, x)).join('');
  } else {
    const hitos = D.filter(x => x.stars >= 100000).slice(0, 10);
    html += '<h2>⭐ Hitos</h2>' + hitos.map(x => {
      const h = Math.floor(x.stars / 100000) * 100000;
      return item('⭐', `supera las ${fmt(h)} estrellas (${fmt(x.stars)})`, x.descripcion_es.split('.')[0] + '.', x);
    }).join('');
  }
  const mov = D.filter(x => (dm[x.full_name] || 0) > 0).sort((a, b) => dm[b.full_name] - dm[a.full_name]).slice(0, 5);
  html += '<h2>🔥 Racha</h2>' + (mov.length
    ? mov.map(x => item('🔥', `sumó +${fmt(dm[x.full_name])} estrellas desde ${CORTE}`, 'En racha', x)).join('')
    : '<p class="mut">Aún sin rachas: aparecen desde el segundo corte semanal.</p>');
  document.getElementById('feed').innerHTML = html;
}
"""


def pagina(nombre, titulo, desc, modulo, cuerpo, js):
    h = BASE.replace("__TITLE__", titulo).replace("__DESC__", desc).replace("__MODULE__", modulo)
    h = h.replace("__BODY__", cuerpo).replace("__PAGEJS__", js)
    h = h.replace("__DB500__", TOP).replace("__DBTRE__", TRE)
    h = h.replace("__DELTAS__", DELTAS).replace("__CORTE__", CORTE)
    open(os.path.join(SITE, nombre), "w", encoding="utf-8").write(h)
    print(nombre, len(h) // 1024, "KB")


pagina("analiticas.html", "Analytics", "Reparto por categoría, lenguaje y licencias del ranking.", "500", ANA_BODY, ANA_JS)
pagina("noticias.html", "Noticias", "Titulares generados del ranking: novedades, hitos y rachas.", "tre", NOT_BODY, NOT_JS)
