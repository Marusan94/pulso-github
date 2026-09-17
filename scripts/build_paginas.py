"""Genera analiticas.html y noticias.html (autonomas, datos embebidos)."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.ranking.historial import deltas, series
from src.ranking.fechas import fecha_corta
DATA = os.path.join(ROOT, "data")
SITE = os.path.join(ROOT, "docs")
TOP_DATA = json.load(open(os.path.join(DATA, "repos.json"), encoding="utf-8"))
TRE_DATA = json.load(open(os.path.join(DATA, "trending.json"), encoding="utf-8"))
TOP = json.dumps(TOP_DATA["repos"], ensure_ascii=False)
TRE = json.dumps(TRE_DATA["repos"], ensure_ascii=False)
HOY = TOP_DATA.get("fecha", "")
FCORTE = fecha_corta(HOY)
UMAMI_URL = (os.environ.get("UMAMI_URL") or "").strip()
UMAMI_ID = (os.environ.get("UMAMI_ID") or "").strip()
UMAMI = ('<script defer src="%s" data-website-id="%s"></script>' % (UMAMI_URL, UMAMI_ID)) if (UMAMI_URL and UMAMI_ID) else ""
SITEURL = (os.environ.get("SITE_URL") or "").strip().rstrip("/")


_dtop = deltas("top", TOP_DATA, DATA)
_dtre = deltas("tre", TRE_DATA, DATA)
DELTAS = json.dumps({"500": _dtop[0], "tre": _dtre[0]}, ensure_ascii=False)
CORTE = _dtop[1]


SERIES = json.dumps({"500": series("top", TOP_DATA, DATA), "tre": series("tre", TRE_DATA, DATA)}, ensure_ascii=False)

BASE = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ — Ranking GitHub</title>
<meta name="description" content="__DESC__">
__CANON__
<meta property="og:title" content="__TITLE__ — Ranking GitHub">
<meta property="og:description" content="__DESC__">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link href="https://fonts.googleapis.com/css2?family=Bitter:wght@400;700;800&family=Work+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#0A1F14;--card:#10281A;--ink:#E9F5EC;--mut:#8FB69C;--acc:#4ADE80;--acctext:#05281A;--line:color-mix(in srgb, #E9F5EC 22%, transparent);--rad:12px;--disp:'Bitter',serif;--tbody:'Work Sans',system-ui,sans-serif}
body{background:var(--bg);color:var(--ink);font-family:var(--tbody);margin:0}
h1,h2,h3{font-family:var(--disp)}
.wrap{max-width:1000px;margin:0 auto;padding:16px}
nav.tabs{display:flex;gap:8px;margin-bottom:6px;flex-wrap:wrap}
nav.tabs a{border:1px solid var(--acc);color:var(--acc);border-radius:999px;padding:8px 16px;text-decoration:none;font-weight:700}
nav.tabs a.on{background:var(--acc);color:var(--acctext)}
.mut{color:var(--mut)}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--rad);padding:14px;margin-bottom:12px}
.seg{display:flex;background:var(--card);border:1px solid var(--line);border-radius:var(--rad);padding:4px;gap:4px;margin:12px 0}
.seg button{flex:1;background:transparent;border:0;color:var(--mut);padding:10px;border-radius:8px;cursor:pointer;font-weight:700;font-family:inherit}
.seg button.on{background:var(--acc);color:var(--acctext)}
.fila{display:grid;grid-template-columns:170px 1fr 90px;gap:8px;align-items:center;margin:6px 0;font-size:14px}
.barra{height:14px;background:var(--bg);border-radius:99px;overflow:hidden;border:1px solid var(--line)}
.barra i{display:block;height:100%;background:var(--acc)}
.num{text-align:right;font-variant-numeric:tabular-nums}
a{color:var(--acc)}
.stats{display:flex;gap:10px;flex-wrap:wrap;margin:12px 0}
.stat{background:var(--card);border:1px solid var(--line);border-radius:var(--rad);padding:10px 16px}
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
<nav class="tabs noprint"><a href="analiticas.html" id="t-ana">◔ Analytics</a><a href="noticias.html" id="t-not">📰 Noticias</a><a href="02-midnight-console.html" id="t-home">⌂ Inicio</a></nav>
__BODY__
</div>
<script>
const DB500 = __DB500__;
const DBTRE = __DBTRE__;
const DELTAS = __DELTAS__;
const SERIES = __SERIES__;
const CORTE = "__CORTE__";
const HOY = '__HOY__';
const PERMISIVAS = ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "CC0-1.0"];
const TEMAS = {
"01-signal-cards": {d:"Archivo", b:"Archivo", bg:"#FAFAF7", card:"#FFFFFF", ink:"#16130E", mut:"#6B6257", acc:"#D63A2F", acctext:"#FFFFFF", rad:"4px"},
"02-midnight-console": {d:"Sora", b:"Sora", bg:"#0A0E14", card:"#11161F", ink:"#E6E1D8", mut:"#8A94A6", acc:"#4ADE80", acctext:"#07130C", rad:"6px"},
"04-ledger-table": {d:"Roboto Slab", b:"Roboto Slab", bg:"#FBFAF7", card:"#FFFFFF", ink:"#1F1B16", mut:"#6E6259", acc:"#1D4ED8", acctext:"#FFFFFF", rad:"2px"},
"05-tide-glass": {d:"Outfit", b:"Outfit", bg:"#0B1B26", card:"rgba(255,255,255,.07)", ink:"#F2F7FA", mut:"#9DB4C0", acc:"#5EEAD4", acctext:"#062A26", rad:"16px"},
"07-control-tower": {d:"DM Sans", b:"DM Sans", bg:"#F2F4FA", card:"#FFFFFF", ink:"#141A2B", mut:"#5B6478", acc:"#4F46E5", acctext:"#FFFFFF", rad:"10px"},
"08-atlas-kanban": {d:"Manrope", b:"Manrope", bg:"#F4F7FA", card:"#FFFFFF", ink:"#10202E", mut:"#5B6B7B", acc:"#0277B6", acctext:"#FFFFFF", rad:"12px"},
"09-phosphor-terminal": {d:"VT323", b:"IBM Plex Mono", bg:"#041008", card:"#06130B", ink:"#B6FFC9", mut:"#3E7A52", acc:"#4ADE80", acctext:"#041008", rad:"0px"},
"11-gallery-wall": {d:"Sora", b:"Hanken Grotesk", bg:"#141210", card:"#1E1B17", ink:"#F5EFE4", mut:"#A89C88", acc:"#F59E0B", acctext:"#231303", rad:"10px"},
"14-block-party": {d:"Archivo Black", b:"Space Mono", bg:"#FFF3D6", card:"#FFFFFF", ink:"#000000", mut:"#3D3D3D", acc:"#FF5C00", acctext:"#1F0E00", rad:"0px"},
"15-plum-material": {d:"Figtree", b:"Figtree", bg:"#F4EFFA", card:"#FFFFFF", ink:"#221B2E", mut:"#6E6580", acc:"#7C3AED", acctext:"#FFFFFF", rad:"16px"},
"16-cave-git": {d:"IBM Plex Mono", b:"IBM Plex Mono", bg:"#0D1117", card:"#161B22", ink:"#E6EDF3", mut:"#8B949E", acc:"#1F6FEB", acctext:"#FFFFFF", rad:"6px"},
"21-podium": {d:"Oswald", b:"Cabin", bg:"#101828", card:"#1A2436", ink:"#F8F3E7", mut:"#9AA3B2", acc:"#FBBF24", acctext:"#231603", rad:"8px"},
"23-night-drive": {d:"Sora", b:"Sora", bg:"#08090D", card:"#101218", ink:"#EDEFF5", mut:"#8E93A3", acc:"#34D399", acctext:"#05281C", rad:"14px"},
"28-abyss": {d:"Chakra Petch", b:"Chakra Petch", bg:"#041E2E", card:"#07293D", ink:"#E8F6FF", mut:"#7FA8BE", acc:"#22D3EE", acctext:"#06252B", rad:"4px"},
"29-evergreen": {d:"Bitter", b:"Work Sans", bg:"#0A1F14", card:"#10281A", ink:"#E9F5EC", mut:"#8FB69C", acc:"#4ADE80", acctext:"#05281A", rad:"12px"},
"30-ember": {d:"DM Serif Display", b:"Karla", bg:"#1A0E08", card:"#241209", ink:"#FBF3E8", mut:"#C0A488", acc:"#F97316", acctext:"#261000", rad:"6px"},
"trending": {d:"Sora", b:"Sora", bg:"#070B14", card:"#111A2E", ink:"#E8ECF5", mut:"#9AA7C2", acc:"#22D3EE", acctext:"#070B14", rad:"12px"}
};
function temaActual(){
  const q = new URLSearchParams(location.search).get('tema');
  return (q && TEMAS[q]) ? q : '';
}
function applyTema(){
  const T = temaActual();
  const th = document.getElementById('t-home');
  if (th) th.href = (T ? T + '.html' : '02-midnight-console.html') + '?mod=' + module;
  if (!T) return;
  const t = TEMAS[T], r = document.documentElement.style;
  r.setProperty('--bg', t.bg); r.setProperty('--card', t.card); r.setProperty('--ink', t.ink);
  r.setProperty('--mut', t.mut); r.setProperty('--acc', t.acc); r.setProperty('--acctext', t.acctext);
  r.setProperty('--rad', t.rad);
  r.setProperty('--disp', "'" + t.d + "',system-ui,sans-serif");
  r.setProperty('--tbody', "'" + t.b + "',system-ui,sans-serif");
  let fl = document.getElementById('temafont');
  if (!fl){ fl = document.createElement('link'); fl.id = 'temafont'; fl.rel = 'stylesheet'; document.head.appendChild(fl); }
  const fams = [...new Set([t.d, t.b])];
  fl.href = 'https://fonts.googleapis.com/css2?' + fams.map(f => 'family=' + f.replace(/ /g, '+') + ':wght@400;600;700').join('&') + '&display=swap';
}
let module = new URLSearchParams(location.search).get('mod') === 'tre' ? 'tre' : "__MODULE__";
function DB(){ return module === '500' ? DB500 : DBTRE; }
function fmt(n){ if (n >= 1000000) return (n/1000000).toFixed(1).replace('.', ',').replace(',0', '') + ' millones'; return n >= 1000 ? (n/1000).toFixed(n >= 100000 ? 0 : 1).replace(/\\.0$/,'') + ' mil' : '' + n; }
function daysOld(iso){ return Math.round((new Date(HOY) - new Date(iso)) / 86400000); }
function age(iso){ const d = daysOld(iso); return d <= 0 ? 'hoy' : d === 1 ? 'ayer' : 'hace ' + d + ' días'; }
function vivo(x){ return !x.archived && (new Date(HOY) - new Date(x.pushed_at || x.created_at || HOY)) / 2592000000 <= 12; }
function ev(n, d){ try { if (window.umami) umami.track(n, d || {}); } catch(e){} }
function setModule(m){
  module = m; page = 0;
  document.getElementById('m500').classList.toggle('on', m === '500');
  document.getElementById('mtre').classList.toggle('on', m === 'tre');
  const ta = document.getElementById('t-ana'), tn = document.getElementById('t-not'), th = document.getElementById('t-home');
  if (ta) ta.href = 'analiticas.html?mod=' + m + (temaActual() ? '&tema=' + temaActual() : '');
  if (tn) tn.href = 'noticias.html?mod=' + m + (temaActual() ? '&tema=' + temaActual() : '');
  if (th) th.href = (temaActual() ? temaActual() + '.html' : '02-midnight-console.html') + '?mod=' + m;
  render();
}
document.getElementById('m500').onclick = () => { ev('modulo', {modulo: '500'}); setModule('500'); };
document.getElementById('mtre').onclick = () => { ev('modulo', {modulo: 'tre'}); setModule('tre'); };
__PAGEJS__
applyTema();
setModule(module);
ev('pagina_vista', {pagina: '__PAGINA__'});
</script>__UMAMI__</body></html>"""

ANA_BODY = """
<p class="mut">500 registros incluidos · corte __FCORTE__</p>
<h1>Analytics</h1>
<div class="seg" role="group" aria-label="Módulo"><button id="m500" class="on">Los 500</button><button id="mtre">Tendencias</button></div>
<div class="stats" id="stats"></div>
<div class="card"><h3>Curva del ranking <small class="mut">— pasa el cursor para previsualizar</small></h3>
<div class="seg" role="group" aria-label="Tipo de curva" style="max-width:420px"><button id="cRank" class="on">Ranking actual</button><button id="cTime">En el tiempo</button></div>
<div class="seg" role="group" aria-label="Cuántos repos muestra la curva" style="max-width:560px" id="nseg"><button data-n="30" class="on">Top 30</button><button data-n="50">Top 50</button><button data-n="100">Top 100</button><button data-n="200">Top 200</button><button data-n="9999">Todos</button></div>
<div id="chartwrap" style="position:relative"><svg id="chart" viewBox="0 0 960 340" style="width:100%;display:block" role="img" aria-label="Gráfica de estrellas"></svg><div id="tip" class="card" style="display:none;position:absolute;pointer-events:none;max-width:280px;z-index:5"></div></div>
<p class="mut" id="chartnote" style="font-size:13px"></p>
<p class="mut" id="chartlegend" style="font-size:13px"></p></div>
<div class="grid2">
<div class="card"><h3>Por categoría</h3><div id="cats"></div></div>
<div class="card"><h3>Lenguajes top</h3><div id="langs"></div></div>
</div>
<div class="grid2">
<div class="card"><h3>Radar por categoría <small class="mut">— puntos numerados por puesto</small></h3><div id="rdwrap" style="position:relative"><div id="radar"></div><div id="rtip" class="card" style="display:none;position:absolute;pointer-events:none;max-width:260px;z-index:5"></div></div><p class="mut" id="rdlegend" style="font-size:13px"></p></div>
<div class="card"><h3>Licencias</h3><div id="lics"></div></div>
</div>
<div class="card"><h3>🔥 Top movidas</h3><div id="mov"></div></div>
<div class="card"><h3>📈 Líderes de crecimiento</h3><p class="mut" id="crecnote" style="font-size:13px"></p><div id="crec"></div><p><button id="bcrec" style="background:transparent;border:1px solid var(--acc);color:var(--acc);border-radius:8px;padding:8px 12px;cursor:pointer;font-weight:700;font-family:inherit">Descargar CSV</button></p></div>
<div class="grid2">
<div class="card"><h3>Distribución de estrellas</h3><div id="hist"></div></div>
<div class="card"><h3>Evolución del repo <small class="mut">— clic en un punto de la curva</small></h3><p class="mut" id="repotitle" style="font-size:13px">Toca un punto de la curva para ver su serie.</p><svg id="reposvg" viewBox="0 0 560 220" style="width:100%;display:block" role="img" aria-label="Serie del repo elegido"></svg></div>
</div>
"""

ANA_JS = """
let page = 0;
document.getElementById('t-ana').classList.add('on');
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
  dibujaCrec(D, dm);
  dibujaHist(D);
  dibujaCurva();
  dibujaRadar();
}
function dibujaCrec(D, dm){
  const rows = D.map(x => ({x, d: dm[x.full_name] || 0})).filter(r => r.d > 0).sort((a, b) => b.d - a.d).slice(0, 10);
  document.getElementById('crecnote').textContent = rows.length ? `Estrellas sumadas desde ${CORTE || HOY}.` : '';
  const box = document.getElementById('crec');
  if (!rows.length){ box.innerHTML = '<p class="mut">Sin movimientos aún: aparecen desde el segundo corte semanal.</p>'; window.__crec = []; return; }
  const m = rows[0].d;
  box.innerHTML = rows.map(r => {
    const prev = r.x.stars - r.d, pp = prev > 0 ? r.d / prev * 100 : 0;
    return `<div class="fila"><span><a href="${r.x.url}" target="_blank" rel="noopener">${r.x.full_name}</a></span><div class="barra"><i style="width:${Math.round(r.d / m * 100)}%"></i></div><span class="num">+${fmt(r.d)} (${pp >= 10 ? Math.round(pp) : pp.toFixed(1)}%)</span></div>`;
  }).join('');
  window.__crec = rows;
}
document.getElementById('bcrec').onclick = () => {
  const rows = window.__crec || [];
  if (!rows.length) return;
  const txt = 'puesto,nombre,estrellas,subida_estrellas,subida_pct,url\\n' + rows.map(r => {
    const prev = r.x.stars - r.d;
    return [r.x.rank, '"' + r.x.full_name + '"', r.x.stars, r.d, (prev > 0 ? (r.d / prev * 100).toFixed(1) : '0'), r.x.url].join(',');
  }).join('\\n');
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([txt], {type: 'text/csv'}));
  a.download = 'lideres-crecimiento-' + module + '.csv'; a.click();
};
function dibujaHist(D){
  const lvs = D.map(x => Math.log10(Math.max(1, x.stars)));
  const mn = Math.min(...lvs), mx = Math.max(...lvs);
  const NB = 8, bins = new Array(NB).fill(0);
  lvs.forEach(v => { const b = Math.floor((v - mn) / ((mx - mn) || 1) * NB); bins[Math.min(NB - 1, b)]++; });
  const m = Math.max(...bins);
  document.getElementById('hist').innerHTML = bins.map((c, i) => {
    const lo = Math.round(Math.pow(10, mn + (mx - mn) * i / NB));
    const hi = Math.round(Math.pow(10, mn + (mx - mn) * (i + 1) / NB));
    return fila(fmt(lo) + ' – ' + fmt(hi), c, m);
  }).join('');
}
function muestraSerie(i){
  const x = (window.__curva || [])[i];
  if (!x) return;
  const pts = ((SERIES[module] || {})[x.full_name] || []);
  document.getElementById('repotitle').innerHTML = `<strong>#${x.rank} ${x.full_name}</strong> — ${fmt(x.stars)} estrellas · <a href="${x.url}" target="_blank" rel="noopener">abrir repo</a>`;
  const svg = document.getElementById('reposvg');
  const W = 560, H = 220, P = 40;
  if (!pts.length){ svg.innerHTML = '<text x="20" y="30" fill="currentColor">Sin datos.</text>'; return; }
  const vals = pts.map(p => p[1]);
  const mn = Math.min(...vals), mx = Math.max(...vals), rg = (mx - mn) || 1;
  const X = j => P + j * (W - 2 * P) / Math.max(1, pts.length - 1);
  const Y = v => H - P - (v - mn) / rg * (H - 2 * P - 40);
  const d = pts.map((p, j) => (j ? 'L' : 'M') + X(j).toFixed(1) + ' ' + Y(p[1]).toFixed(1)).join('');
  let h = `<path d="${d}" fill="none" stroke="currentColor" stroke-width="2.5"/>`;
  h += pts.map((p, j) => `<circle cx="${X(j).toFixed(1)}" cy="${Y(p[1]).toFixed(1)}" r="4.5" fill="currentColor"><title>${p[0]}: ${fmt(p[1])}</title></circle>`).join('');
  h += `<text x="${P}" y="${H - 12}" fill="currentColor" font-size="13" opacity=".6">${pts[0][0]}</text>`;
  h += `<text x="${W - P}" y="${H - 12}" fill="currentColor" font-size="13" text-anchor="end" opacity=".6">${pts[pts.length - 1][0]} · ${fmt(vals[vals.length - 1])}</text>`;
  svg.innerHTML = h;
}
let curvaModo = 'rank';
let curvaN = 30;
document.querySelectorAll('#nseg button').forEach(b => b.onclick = () => {
  document.querySelectorAll('#nseg button').forEach(x => x.classList.remove('on'));
  b.classList.add('on'); curvaN = +b.dataset.n; ev('top_tamano', {n: curvaN}); dibujaCurva();
});
document.getElementById('cRank').onclick = () => { curvaModo = 'rank'; document.getElementById('cRank').classList.add('on'); document.getElementById('cTime').classList.remove('on'); dibujaCurva(); };
document.getElementById('cTime').onclick = () => { curvaModo = 'time'; document.getElementById('cTime').classList.add('on'); document.getElementById('cRank').classList.remove('on'); dibujaCurva(); };
function dibujaCurva(){
  const svg = document.getElementById('chart'), tip = document.getElementById('tip'), note = document.getElementById('chartnote');
  const W = 960, H = 340, P = 64;
  const acc = getComputedStyle(document.body).getPropertyValue('--acc') || '#4ADE80';
  svg.innerHTML = ''; tip.style.display = 'none';
  if (curvaModo === 'time'){
    const S = SERIES[module] || {};
    const conHist = Object.keys(S).filter(k => (S[k] || []).length > 1);
    if (!conHist.length){ note.textContent = 'La vista en el tiempo se activa desde el segundo corte semanal: hoy hay un solo punto por repo.'; return; }
    const fechas = [...new Set([].concat(...conHist.map(k => S[k].map(p => p[0]))))].sort();
    const top = conHist.map(k => ({k, v: S[k][S[k].length - 1][1]})).sort((a, b) => b.v - a.v).slice(0, 8);
    const vals = [].concat(...top.map(t => S[t.k].map(p => p[1])));
    const mn = Math.min(...vals), mx = Math.max(...vals), rg = (mx - mn) || 1;
    const X = i => P + i * (W - 2 * P) / Math.max(1, fechas.length - 1);
    const Y = v => H - P - (v - mn) / rg * (H - 2 * P);
    let h = `<defs><linearGradient id="gg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${acc}" stop-opacity=".35"/><stop offset="1" stop-color="${acc}" stop-opacity="0"/></linearGradient></defs>`;
    h += fechas.map((f, i) => `<text x="${X(i)}" y="${H - 12}" fill="currentColor" font-size="16" text-anchor="middle" opacity=".6">${f.slice(5)}</text>`).join('');
    const pal = ['#4ADE80', '#22D3EE', '#FBBF24', '#F472B6', '#A78BFA', '#FB7185', '#34D399', '#F97316'];
    top.forEach((t, j) => {
      const pts = fechas.map(f => { const p = S[t.k].filter(p2 => p2[0] === f).pop(); return p ? p[1] : null; });
      let d = '', started = false, area = '';
      pts.forEach((v, i) => { if (v == null) return; d += (started ? 'L' : 'M') + X(i).toFixed(1) + ' ' + Y(v).toFixed(1); started = true; });
      const line = `<path d="${d}" fill="none" stroke="${pal[j % 8]}" stroke-width="2.5"><title>${t.k}</title></path>`;
      const dots = pts.map((v, i) => v == null ? '' : `<circle cx="${X(i).toFixed(1)}" cy="${Y(v).toFixed(1)}" r="4" fill="${pal[j % 8]}"><title>${t.k}: ${fmt(v)}</title></circle>`).join('');
      h += line + dots + `<text x="${W - P + 6}" y="${Y(S[t.k][S[t.k].length-1][1]).toFixed(1)}" fill="${pal[j % 8]}" font-size="15">${t.k.split('/')[1] || t.k}</text>`;
    });
    svg.innerHTML = h;
    note.textContent = 'Evolución por corte semanal (top 8 del módulo). Pasa el cursor sobre cada línea para ver el repo.';
    document.getElementById('chartlegend').textContent = `Viendo top 8 de ${module === '500' ? 'Los 500' : 'Tendencias'} en ${fechas.length} cortes · del ${fechas[0]} al ${fechas[fechas.length - 1]}.`;
    return;
  }
  const D = DB().slice().sort((a, b) => b.stars - a.stars).slice(0, Math.min(curvaN, DB().length));
  const lvs = D.map(x => Math.log10(Math.max(1, x.stars)));
  const mn = Math.min(...lvs), mx = Math.max(...lvs), rg = (mx - mn) || 1;
  const X = i => P + i * (W - 2 * P) / Math.max(1, D.length - 1);
  const Y = v => H - P - (v - mn) / rg * (H - 2 * P);
  const pts = D.map((x, i) => `${X(i).toFixed(1)},${Y(lvs[i]).toFixed(1)}`).join(' ');
  const chico = D.length <= 50, rDot = D.length > 200 ? 2.5 : 4.5;
  let h = `<defs><linearGradient id="gg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${acc}" stop-opacity=".4"/><stop offset="1" stop-color="${acc}" stop-opacity="0"/></linearGradient></defs>`;
  h += `<polygon points="${P},${H - P} ${pts} ${W - P},${H - P}" fill="url(#gg)"/>`;
  h += `<polyline points="${pts}" fill="none" stroke="${acc}" stroke-width="2.5"/>`;
  [0, 1, 2, 3].forEach(j => {
    const v = mn + rg * j / 3, y = Y(v);
    h += `<line x1="${P}" y1="${y}" x2="${W - P}" y2="${y}" stroke="currentColor" opacity=".15"/><text x="${P - 6}" y="${y + 5}" fill="currentColor" font-size="14" text-anchor="end" opacity=".6">${fmt(Math.round(Math.pow(10, v)))}</text>`;
  });
  const pasoX = Math.ceil(D.length / 6);
  for (let i = 0; i < D.length; i += pasoX){
    h += `<text x="${X(i).toFixed(1)}" y="${H - P + 22}" fill="currentColor" font-size="13" text-anchor="middle" opacity=".6">#${D[i].rank}</text>`;
  }
  h += D.map((x, i) => `<circle cx="${X(i).toFixed(1)}" cy="${Y(lvs[i]).toFixed(1)}" r="${rDot}" fill="var(--card, #10281A)" stroke="${acc}" stroke-width="2.5" style="pointer-events:none"/>`).join('');
  const nNom = chico ? Math.min(10, D.length) : 5;
  h += D.slice(0, nNom).map((x, i) => {
    const xx = X(i).toFixed(1), yy = Y(lvs[i]).toFixed(1);
    return `<text x="${xx}" y="${(Y(lvs[i]) - 8).toFixed(1)}" fill="currentColor" font-size="12" font-weight="700" text-anchor="start" transform="rotate(-28 ${xx} ${yy})">#${x.rank} ${(x.full_name.split('/')[1] || '').slice(0, 20)}</text>`;
  }).join('');
  h += D.map((x, i) => `<circle data-i="${i}" cx="${X(i).toFixed(1)}" cy="${Y(lvs[i]).toFixed(1)}" r="11" fill="transparent"/>`).join('');
  svg.innerHTML = h;
  note.textContent = `Top ${D.length} del módulo en escala logarítmica: cae rápido y la cola es larga. Eje X = puesto, eje Y = estrellas.`;
  document.getElementById('chartlegend').textContent = `Viendo ${D.length} repos de ${module === '500' ? 'Los 500' : 'Tendencias'} · líder ${D[0].full_name} con ${fmt(D[0].stars)} estrellas · corte ${HOY}.`;
  window.__curva = D;
  svg.querySelectorAll('circle').forEach(c => {
    c.addEventListener('mousemove', e => {
      const x = window.__curva[+c.getAttribute('data-i')];
      tip.innerHTML = `<strong>#${x.rank} ${x.full_name}</strong><br>${fmt(x.stars)} estrellas · ${x.language}<br><small>${(x.descripcion_es || '').slice(0, 120)}</small><br><img src="https://opengraph.githubassets.com/1/${x.full_name}" alt="" style="width:100%;border-radius:8px;margin-top:6px" loading="lazy"><br><a href="${x.url}" target="_blank" rel="noopener">Abrir repo</a>`;
      tip.style.display = 'block';
      const r = document.getElementById('chartwrap').getBoundingClientRect();
      tip.style.left = Math.min(e.clientX - r.left + 14, r.width - 290) + 'px';
      tip.style.top = (e.clientY - r.top + 14) + 'px';
    });
    c.addEventListener('mouseleave', () => tip.style.display = 'none');
    c.addEventListener('click', () => muestraSerie(+c.getAttribute('data-i')));
  });
}
function dibujaRadar(){
  const box = document.getElementById('radar'), tip = document.getElementById('rtip');
  const cats = ["IA/LLM", "Frontend", "Educación/Recursos", "Backend/DevOps", "Templates", "Seguridad", "DevTools"];
  const D = DB();
  const S = 560, C = 280, R = 205;
  const lvs = D.map(x => Math.log10(Math.max(1, x.stars)));
  const mn = Math.min(...lvs), mx = Math.max(...lvs), rg = (mx - mn) || 1;
  const radio = s => R - (Math.log10(Math.max(1, s)) - mn) / rg * (R - 34);
  const pal = ['#4ADE80', '#22D3EE', '#FBBF24', '#F472B6', '#A78BFA', '#FB7185', '#34D399'];
  let h = `<svg viewBox="-40 -20 640 600" style="width:100%;display:block" role="img" aria-label="Radar de repositorios por categoría">`;
  h += `<circle cx="${C}" cy="${C}" r="16" fill="none" stroke="currentColor" opacity=".5"/><text x="${C}" y="${C + 5}" fill="currentColor" font-size="13" text-anchor="middle" opacity=".7">TOP</text>`;
  [0.35, 0.7].forEach(f => { h += `<circle cx="${C}" cy="${C}" r="${(R * f).toFixed(1)}" fill="none" stroke="currentColor" opacity=".15"/>`; });
  cats.forEach((c, i) => {
    const a0 = -Math.PI / 2 + (i - 0.5) * 2 * Math.PI / cats.length;
    const a1 = -Math.PI / 2 + (i + 0.5) * 2 * Math.PI / cats.length;
    const x0 = C + R * Math.cos(a0), y0 = C + R * Math.sin(a0), x1 = C + R * Math.cos(a1), y1 = C + R * Math.sin(a1);
    h += `<path d="M${C} ${C} L${x0.toFixed(1)} ${y0.toFixed(1)} A${R} ${R} 0 0 1 ${x1.toFixed(1)} ${y1.toFixed(1)} Z" fill="${pal[i % 7]}" fill-opacity="${i % 2 ? 0.05 : 0.1}"/>`;
    h += `<line x1="${C}" y1="${C}" x2="${x1.toFixed(1)}" y2="${y1.toFixed(1)}" stroke="currentColor" opacity=".2"/>`;
    const am = -Math.PI / 2 + i * 2 * Math.PI / cats.length;
    const lx = C + (R + 34) * Math.cos(am), ly = C + (R + 34) * Math.sin(am);
    h += `<text x="${lx.toFixed(1)}" y="${ly.toFixed(1)}" fill="currentColor" font-size="15" text-anchor="middle">${c.split('/')[0]}</text>`;
  });
  const usados = [];
  cats.forEach((c, i) => {
    const top = D.filter(x => x.categoria === c).sort((a, b) => b.stars - a.stars).slice(0, 6);
    const am = -Math.PI / 2 + i * 2 * Math.PI / cats.length, spread = (2 * Math.PI / cats.length) * 0.62;
    top.forEach((x, j) => {
      const an = am + (top.length > 1 ? (j / (top.length - 1) - 0.5) * spread : 0);
      const r = Math.min(R - 8, Math.max(30, radio(x.stars) + (j % 2 ? 9 : -9)));
      const cx = C + r * Math.cos(an), cy = C + r * Math.sin(an);
      const grande = x.rank <= 3;
      usados.push({x, cx, cy});
      h += `<circle data-k="${x.full_name}" cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="${grande ? 11 : 8}" fill="${pal[i % 7]}" fill-opacity=".25" stroke="${pal[i % 7]}" stroke-width="2" style="cursor:pointer"/>`;
      h += `<text x="${cx.toFixed(1)}" y="${(cy + 4).toFixed(1)}" font-size="${grande ? 11 : 9}" font-weight="800" text-anchor="middle" fill="currentColor" style="pointer-events:none">${x.rank}</text>`;
    });
  });
  h += `</svg>`;
  box.innerHTML = h;
  document.getElementById('rdlegend').textContent = `Cada punto es un repo y el número es su puesto. Más cerca del centro = más estrellas. Sectores = categorías. Mostrando ${usados.length} repos (top 6 por categoría).`;
  window.__rd = {};
  usados.forEach(u => window.__rd[u.x.full_name] = u.x);
  box.querySelectorAll('circle[data-k]').forEach(c => {
    const show = e => {
      const x = window.__rd[c.getAttribute('data-k')];
      const lic = !x.license || x.license === 'NOASSERTION' || x.license === '—' ? 'sin dato' : x.license;
      tip.innerHTML = `<strong>#${x.rank} ${x.full_name}</strong><br>${fmt(x.stars)} estrellas · ${x.language} · ${lic}<br><small>${(x.descripcion_es || '').slice(0, 110)}</small><br><img src="https://opengraph.githubassets.com/1/${x.full_name}" alt="" style="width:100%;border-radius:8px;margin-top:6px" loading="lazy"><br><a href="${x.url}" target="_blank" rel="noopener">Abrir repo</a>`;
      tip.style.display = 'block';
      const r = document.getElementById('rdwrap').getBoundingClientRect();
      tip.style.left = Math.min(Math.max(0, e.clientX - r.left + 14), r.width - 270) + 'px';
      tip.style.top = (e.clientY - r.top + 14) + 'px';
    };
    c.addEventListener('mousemove', show);
    c.addEventListener('mouseleave', () => tip.style.display = 'none');
  });
}
"""

NOT_BODY = """
<p class="mut">Titulares generados de tus datos · corte __FCORTE__</p>
<h1>Noticias</h1>
<div class="seg" role="group" aria-label="Módulo"><button id="m500" class="on">Los 500</button><button id="mtre">Tendencias</button></div>
<div id="feed"></div>
"""

NOT_JS = """
let page = 0;
document.getElementById('t-not').classList.add('on');
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
    h = h.replace("__DELTAS__", DELTAS).replace("__SERIES__", SERIES).replace("__CORTE__", CORTE)
    h = h.replace("__HOY__", HOY).replace("__FCORTE__", FCORTE)
    h = h.replace("__PAGINA__", nombre).replace("__UMAMI__", UMAMI)
    h = h.replace("__CANON__", ('<link rel="canonical" href="%s/%s">\n<meta property="og:url" content="%s/%s">' % (SITEURL, nombre, SITEURL, nombre)) if SITEURL else "")
    open(os.path.join(SITE, nombre), "w", encoding="utf-8").write(h)
    print(nombre, len(h) // 1024, "KB")


pagina("analiticas.html", "Analytics", "Reparto por categoría, lenguaje y licencias del ranking.", "500", ANA_BODY, ANA_JS)
pagina("noticias.html", "Noticias", "Titulares generados del ranking: novedades, hitos y rachas.", "tre", NOT_BODY, NOT_JS)
