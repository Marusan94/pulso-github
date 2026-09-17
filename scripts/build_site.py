import glob
import json
import os
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.ranking.historial import deltas, series
from src.ranking.fechas import fecha_corta, dias_atras
DATA = os.path.join(ROOT, "data")
SITE = os.path.join(ROOT, "docs")
SRC = SITE
TOP_DATA = json.load(open(os.path.join(DATA, "repos.json"), encoding="utf-8"))
TRE_DATA = json.load(open(os.path.join(DATA, "trending.json"), encoding="utf-8"))
TOP = json.dumps(TOP_DATA["repos"], ensure_ascii=False)
TRE = json.dumps(TRE_DATA["repos"], ensure_ascii=False)
print("top:", len(TOP) // 1024, "KB | tre:", len(TRE) // 1024, "KB")
HOY = TOP_DATA.get("fecha", "")
FCORTE = fecha_corta(HOY)
DMIN = dias_atras(HOY, 31)
UMAMI_URL = (os.environ.get("UMAMI_URL") or "").strip()
UMAMI_ID = (os.environ.get("UMAMI_ID") or "").strip()
UMAMI = ('<script defer src="%s" data-website-id="%s"></script>' % (UMAMI_URL, UMAMI_ID)) if (UMAMI_URL and UMAMI_ID) else ""
SITEURL = (os.environ.get("SITE_URL") or "").strip().rstrip("/")
if UMAMI:
    print("umami: tracker de producción activado")
else:
    print("umami: desactivado (build local, sin UMAMI_URL/UMAMI_ID)")


DELTAS_TOP, CORTE_TOP, RANK_TOP = deltas("top", TOP_DATA, DATA)
DELTAS_TRE, CORTE_TRE, RANK_TRE = deltas("tre", TRE_DATA, DATA)
DELTAS = json.dumps({"500": DELTAS_TOP, "tre": DELTAS_TRE}, ensure_ascii=False)
RANKSPREV = json.dumps({"500": RANK_TOP, "tre": RANK_TRE}, ensure_ascii=False)
CORTES = json.dumps({"actual": TOP_DATA.get("fecha", ""), "anterior": CORTE_TOP or ""})


SERIES = json.dumps({"500": series("top", TOP_DATA, DATA), "tre": series("tre", TRE_DATA, DATA)}, ensure_ascii=False)
print("series: puntos por repo (cortes:", len(glob.glob(os.path.join(DATA, "history", "*.json"))), ")")
print("deltas:", len([v for v in DELTAS_TOP.values() if v]), "con cambio (corte previo:", CORTE_TOP or "ninguno", ")")

# fid, titulo, layout, extra_css, extra_hero
FILES = [
("01-signal-cards", "Signal", "cards", ".card{border-left:4px solid var(--acc)} .rn{font-family:mono;font-size:22px;color:var(--acc)}", ""),
("02-midnight-console", "Consola", "table", ".dots span{display:inline-block;width:10px;height:10px;border-radius:50%;background:#2A3550;margin-right:6px}", "<div class='dots noprint'><span></span><span></span><span></span></div>"),
("04-ledger-table", "Libro", "table", "td.num{text-align:right} tbody tr:nth-child(even){background:#0D1526}", ""),
("05-tide-glass", "Marea", "cards", ".card{background:rgba(17,26,46,.72);backdrop-filter:blur(6px)}", ""),
("07-control-tower", "Torre", "split", ".live{display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--acc)}", "<p class='mut'><span class='live'></span> base local, sin internet salvo vistas previas</p>"),
("08-atlas-kanban", "Atlas", "kanban", ".colh{border-bottom:2px solid var(--acc);padding-bottom:4px}", ""),
("09-phosphor-terminal", "Fósforo", "table", ".scan{height:6px;background:repeating-linear-gradient(0deg,var(--acc) 0 1px,transparent 1px 3px);opacity:.25;margin:8px 0} td{font-family:mono}", "<div class='scan'></div><p class='mut'>> consultando base local de 500 registros...</p>"),
("11-gallery-wall", "Galería", "bento", "img.prev{min-height:120px;object-fit:cover}", ""),
("14-block-party", "Bloque", "cards", ".card{border:2px solid var(--acc);box-shadow:5px 5px 0 var(--acc)}", ""),
("15-plum-material", "Pluma", "cards", ".card{border-radius:20px} h1{letter-spacing:.01em}", ""),
("16-cave-git", "Cueva", "list", ".card{background:transparent;border:0;border-bottom:1px solid #2A3550;border-radius:0}", ""),
("21-podium", "Podio", "podium", ".medal{font-size:38px;font-weight:800;color:var(--acc)}", ""),
("23-night-drive", "Nocturna", "cards", "@media(prefers-reduced-motion:no-preference){.card{animation:up .35s ease both} .card:nth-child(2){animation-delay:.05s} .card:nth-child(3){animation-delay:.1s} .card:nth-child(4){animation-delay:.15s} @keyframes up{from{opacity:0;transform:translateY(8px)}}}", ""),
("28-abyss", "Abismo", "table", ".twrap{background:#0A1424;border-radius:12px}", ""),
("29-evergreen", "Perenne", "cards", ".card{border-style:double;border-width:4px}", ""),
("30-ember", "Brasa", "bento", ".lead{grid-column:1/-1} .lead img.prev{max-height:260px;object-fit:cover}", ""),
("trending", "Tendencias", "cards", ".age{font-size:15px}", ""),
]

TPL = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pulso GitHub · __TITLE__</title>
<meta name="description" content="__DESC__">
__CANON__
<meta property="og:title" content="Pulso GitHub · __TITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary">
__FONTLINK__
<style>
:root{--bg:__BG__;--card:__CARD__;--ink:__INK__;--mut:__MUT__;--acc:__ACC__;--acctext:__ACCTEXT__;--rad:__RAD__;--line:color-mix(in srgb, var(--ink) 20%, transparent)}
body{background:var(--bg);color:var(--ink);font-family:'__BODY__',system-ui,sans-serif;margin:0}
.mono{font-family:'__MONO__',monospace}
.wrap{max-width:1100px;margin:0 auto;padding:16px}
h1{font-family:'__DISP__',system-ui,sans-serif;font-weight:800;letter-spacing:-.01em;margin:6px 0}
.mut{color:var(--mut)}
.seg{display:flex;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:4px;gap:4px;margin:12px 0;flex-wrap:wrap}
.seg button{flex:1;background:transparent;border:0;color:var(--mut);padding:10px;border-radius:8px;cursor:pointer;font-weight:600;font-family:inherit;white-space:nowrap}
.seg button.on{background:var(--acc);color:var(--acctext)}
.seg input{background-color:color-mix(in srgb, var(--ink) 6%, transparent);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px;font-family:inherit}
.bar{display:flex;gap:8px;flex-wrap:wrap;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px;position:sticky;top:8px;z-index:5;align-items:center}
.bar label{color:var(--ink);font-weight:600}
.bar input,.bar select{background:color-mix(in srgb, var(--ink) 6%, transparent);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px 10px;font-family:inherit}
.bar select option{background:var(--card);color:var(--ink)}

/* Revertir cambios */
/* .bar{display:flex;gap:8px;flex-wrap:wrap;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px;position:sticky;top:8px;z-index:5;align-items:center}
.bar label{color:var(--ink);font-weight:600}
.bar input,.bar select{background:color-mix(in srgb, var(--ink) 6%, transparent);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px 10px;font-family:inherit} */
.bar input{flex:1;min-width:160px}
.dl{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0;align-items:center}
.dl button{background:transparent;border:1px solid var(--acc);color:var(--acc);border-radius:8px;padding:8px 12px;cursor:pointer;font-weight:600;font-family:inherit}
.dl a{color:var(--acc)}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--rad);padding:12px}
.pick{border:1px solid var(--acc);color:var(--acc);background:transparent;border-radius:8px;padding:6px 10px;cursor:pointer;font-weight:700;font-family:inherit;margin-top:6px}
.pick.on{background:var(--acc);color:var(--acctext)}
.modowrap{position:relative;display:inline-block}
#modobtn{border:1px solid var(--acc);color:var(--acc);background:transparent;border-radius:999px;padding:8px 16px;cursor:pointer;font-weight:700;font-family:inherit}
#modomenu{display:none;position:absolute;top:110%;left:0;z-index:20;min-width:230px;max-height:320px;overflow:auto;padding:6px}
#modomenu.open{display:block}
#modomenu a{display:flex;justify-content:space-between;gap:8px;padding:8px 10px;border-radius:8px;text-decoration:none;color:var(--ink)}
#modomenu a:hover{background:color-mix(in srgb, var(--ink) 8%, transparent)}
#modomenu a.cur{font-weight:800}
.dot{width:12px;height:12px;border-radius:50%;display:inline-block;border:1px solid var(--line);flex-shrink:0;align-self:center}
.bdg{display:inline-block;font-size:11px;padding:2px 8px;border:1px solid var(--line);border-radius:999px;margin:1px 2px;color:var(--mut)}
.age{font-family:'JetBrains Mono',monospace;background:var(--acc);color:var(--acctext);font-weight:700;border-radius:8px;padding:4px 10px;white-space:nowrap}
a{color:var(--acc)}
img.prev{width:100%;border-radius:8px;display:block;border:1px solid var(--line)}
.pg{display:flex;gap:8px;align-items:center;margin:10px 0}
.pg button{background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:6px 12px;cursor:pointer;font-family:inherit}
table{width:100%;border-collapse:collapse;font-size:14px}
th,td{text-align:left;padding:8px;border-top:1px solid var(--line);vertical-align:top}
th{color:var(--mut);font-weight:600}
td.num{font-family:'JetBrains Mono',monospace;white-space:nowrap}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
@media(max-width:760px){.grid,.grid3{grid-template-columns:1fr}}
:focus-visible{outline:3px solid var(--acc);outline-offset:2px}
__EXTRA_CSS__
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
@media print{.bar,.pg,.dl,.seg,.noprint{display:none!important}body{background:#fff;color:#000}.card{border-color:#000;break-inside:avoid}}
</style></head>
<body><div class="wrap">
<nav class="noprint" aria-label="Secciones" style="display:flex;gap:8px;margin-bottom:4px"><a id="t-ana" href="analiticas.html" style="border:1px solid var(--acc);color:var(--acc);border-radius:999px;padding:8px 16px;text-decoration:none;font-weight:700">◔ Analytics</a><a id="t-not" href="noticias.html" style="border:1px solid var(--acc);color:var(--acc);border-radius:999px;padding:8px 16px;text-decoration:none;font-weight:700">📰 Noticias</a></nav>
<p class="mut mono">500 registros incluidos en este archivo &middot; corte __FCORTE__ &middot; funciona sin internet salvo vistas previas</p>
<h1>Pulso GitHub</h1>
<p class="mut">Busca, filtra y abre cada repositorio con su vista previa.</p>
__EXTRA_HERO__
<div class="modowrap noprint"><button id="modobtn" aria-haspopup="true">◐ Tema: __TITLE__ ▾</button><div id="modomenu" class="card" role="menu"></div></div>
<div class="seg noprint" role="group" aria-label="Módulo"><button id="m500" class="on">Los 500</button><button id="mtre">Tendencias</button></div>
<div class="seg noprint" id="dates" style="display:none" role="group" aria-label="Rango de fechas">
<button data-r="5" class="on">Últimos 5 días</button><button data-r="15">Últimos 15 días</button><button data-r="31">El mes</button>
<span class="mut" style="align-self:center">o por un día exacto:</span><input type="date" id="d" min="__DMIN__" max="__HOY__" aria-label="Filtrar por día exacto">
</div>
<div class="bar">
<label class="mut" for="q">Buscar</label><input id="q" placeholder="Por ejemplo: agentes, python, editores...">
<label class="mut" for="c">Categoría</label><select id="c"><option value="">Todas</option></select>
<label class="mut" for="s">Ordenar por</label><select id="s"><option value="stars">Estrellas</option><option value="new">Más nuevos</option><option value="forks">Bifurcaciones</option><option value="up">Mayor subida</option></select>
<div style="flex-basis:100%;height:0"></div>
<label class="mut" for="lic">Licencia</label><select id="lic"><option value="">Todas</option><option value="MIT">MIT</option><option value="perm">Permisivas (MIT/Apache/BSD)</option><option value="copy">Copyleft (revisar)</option></select>
<label class="mut"><input type="checkbox" id="vivo"> Solo vivos</label>
<label class="mut"><input type="checkbox" id="noaw"> Sin awesome-lists</label>
<span id="n" class="mut"></span></div>
<div class="dl noprint">
<button id="bcsv">CSV</button><button id="bxlsx">Excel (filtrado)</button>
<button id="bjson">JSON</button><button id="bpdf">PDF</button>
<a id="fullx" href="top500.xlsx">Excel completo</a></div>
<div class="dl noprint" id="favbar">
<button id="bfav">★ Mis elegidos (<span id="favc">0</span>)</button>
<button id="fxlsx">Excel elegidos</button><button id="fpdf">PDF elegidos</button><button id="fcsv">CSV elegidos</button>
<button id="fclear">Limpiar</button><span id="favmsg" class="mut"></span></div>
<div id="mov"></div>
<div class="pg"><button id="prev">&lsaquo;</button><span id="p" class="mut"></span><button id="next">&rsaquo;</button></div>
<div id="g"></div>
<div class="pg"><button id="prev2">&lsaquo;</button><span id="p2" class="mut"></span><button id="next2">&rsaquo;</button></div>
<p class="mut noprint" style="text-align:center;font-size:13px"><a href="como-esta-hecho.html">Cómo está hecho este ranking</a></p>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
<script>
const DB500 = __DB500__;
const DELTAS = __DELTAS__;
const SERIES = __SERIES__;
const CORTES = __CORTES__;
const DBTRE = __DBTRE__;
const LAYOUT = "__LAYOUT__";
const RANKSPREV = __RANKSPREV__;
const HOY = '__HOY__';
let module = "__MODULE__", range = 5, exactDay = '', F = [], page = 0, showFav = false;
let FAV = {};
try { FAV = JSON.parse(localStorage.getItem('gr-favs-v1') || '{}'); } catch(e){ FAV = {}; }
function saveFav(){ try { localStorage.setItem('gr-favs-v1', JSON.stringify(FAV)); } catch(e){} }
function favCount(){ return Object.keys(FAV).length; }
function updateFavUI(){
  document.getElementById('favc').textContent = favCount();
  document.getElementById('bfav').innerHTML = showFav ? 'Ver todos' : '★ Mis elegidos (<span id="favc">' + favCount() + '</span>)';
  const m = document.getElementById('favmsg');
  if (m) m.textContent = showFav ? 'Viendo solo tus elegidos.' : '';
}
function movBadge(x){
  if (!CORTES.anterior) return '';
  const pr = (RANKSPREV[module] || {})[x.full_name];
  if (!pr) return `<span class="bdg">🆕 nuevo en el ranking</span>`;
  const d = pr - x.rank;
  if (d > 0) return `<span class="bdg" style="border-color:#16a34a;color:#16a34a;font-weight:800">▲${d} puestos</span>`;
  if (d < 0) return `<span class="bdg" style="border-color:#dc2626;color:#dc2626;font-weight:800">▼${-d} puestos</span>`;
  return `<span class="bdg">═ igual</span>`;
}
function rankGain(x){
  const pr = (RANKSPREV[module] || {})[x.full_name];
  return pr ? pr - x.rank : -9999;
}
function favRows(){
  const out = [];
  Object.keys(FAV).forEach(k => {
    const parts = k.split('|'), src = parts[0] === 'tre' ? DBTRE : DB500;
    const hit = src.filter(x => x.full_name === parts.slice(1).join('|'));
    if (hit.length) out.push(hit[0]);
  });
  return out;
}
const PER = 50, g = document.getElementById('g');
function DB(){ return module === '500' ? DB500 : DBTRE; }
function daysOld(iso){ return Math.round((new Date(HOY) - new Date(iso)) / 86400000); }
function age(iso){ const d = daysOld(iso); return d <= 0 ? 'hoy' : d === 1 ? 'ayer' : 'hace ' + d + ' días'; }
function fmt(n){ if (n >= 1000000) return (n/1000000).toFixed(1).replace('.', ',').replace(',0', '') + ' millones'; return n >= 1000 ? (n/1000).toFixed(n >= 100000 ? 0 : 1).replace(/\\.0$/,'') + ' mil' : '' + n; }
function fillCats(){
  const csel = document.getElementById('c'), cur = csel.value;
  csel.innerHTML = '<option value="">Todas</option>';
  [...new Set(DB().map(x => x.categoria))].sort().forEach(c => {
    const o = document.createElement('option'); o.value = c; o.textContent = c; csel.appendChild(o);
  });
  if ([...csel.options].some(o => o.value === cur)) csel.value = cur;
}
function ev(n, d){ try { if (window.umami) umami.track(n, d || {}); } catch(e){} }
function setModule(m){
  module = m; page = 0; exactDay = '';
  const dd = document.getElementById('d'); if (dd) dd.value = '';
  document.getElementById('m500').classList.toggle('on', m === '500');
  document.getElementById('mtre').classList.toggle('on', m === 'tre');
  document.getElementById('dates').style.display = m === 'tre' ? 'flex' : 'none';
  document.getElementById('fullx').href = m === '500' ? 'top500.xlsx' : 'trending.xlsx';
  document.getElementById('fullx').textContent = m === '500' ? 'Excel completo (500 repositorios)' : 'Excel completo (200 repositorios)';
  const ta = document.getElementById('t-ana'), tn = document.getElementById('t-not');
  if (ta) ta.href = 'analiticas.html?mod=' + m + '&tema=__FILE__';
  if (tn) tn.href = 'noticias.html?mod=' + m + '&tema=__FILE__';
  fillCats(); apply();
}
document.getElementById('m500').onclick = () => { ev('modulo', {modulo: '500'}); setModule('500'); };
document.getElementById('mtre').onclick = () => { ev('modulo', {modulo: 'tre'}); setModule('tre'); };
document.querySelectorAll('#dates button').forEach(b => b.onclick = () => {
  document.querySelectorAll('#dates button').forEach(x => x.classList.remove('on'));
  b.classList.add('on'); range = +b.dataset.r; exactDay = '';
  document.getElementById('d').value = ''; page = 0; apply();
});
document.getElementById('d').onchange = e => {
  exactDay = e.target.value; page = 0;
  if (exactDay) document.querySelectorAll('#dates button').forEach(x => x.classList.remove('on'));
  apply();
};
const PERMISIVAS = ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "CC0-1.0"];
function esCopyleft(lic){ return /GPL|AGPL|LGPL/i.test(lic || ""); }
function mesesSinActividad(x){ const f = x.pushed_at || x.created_at || HOY; return (new Date(HOY) - new Date(f)) / 2592000000; }
function veredicto(x){
  if (x.archived || esCopyleft(x.license)) return "⚠ revisar: " + (x.archived ? "archivado" : "licencia copyleft");
  if (mesesSinActividad(x) > 12) return "⚠ revisar: sin actividad 12+ meses";
  if (PERMISIVAS.includes(x.license)) return "✓ adoptable";
  return "· sin veredicto";
}
function apply(){
  const q = document.getElementById('q').value.toLowerCase(),
        c = document.getElementById('c').value, s = document.getElementById('s').value,
        lic = document.getElementById('lic').value,
        vivo = document.getElementById('vivo').checked,
        noaw = document.getElementById('noaw').checked;
  F = DB().filter(x => {
    if (c && x.categoria !== c) return false;
    if (lic === "MIT" && x.license !== "MIT") return false;
    if (lic === "perm" && !PERMISIVAS.includes(x.license)) return false;
    if (lic === "copy" && !esCopyleft(x.license)) return false;
    if (vivo && (x.archived || mesesSinActividad(x) > 12)) return false;
    if (noaw && x.tipo === "awesome-list") return false;
    if (module === 'tre'){
      if (exactDay){ if (x.created_at !== exactDay) return false; }
      else if (daysOld(x.created_at) >= range) return false;
    }
    return (x.full_name + ' ' + (x.descripcion_es||'') + ' ' + (x.description||'') + ' ' + x.language).toLowerCase().includes(q);
  });
  F.sort((a,b) => s === 'forks' ? b.forks - a.forks : s === 'new' ? (b.created_at||b.pushed_at||'').localeCompare(a.created_at||a.pushed_at||'') : s === 'up' ? ((rankGain(b) - rankGain(a)) || (((DELTAS[module]||{})[b.full_name]||0) - ((DELTAS[module]||{})[a.full_name]||0))) : b.stars - a.stars);
  page = 0; render();
}
['q','c','s','lic','vivo','noaw'].forEach(id => document.getElementById(id).addEventListener('input', apply));
function go(d){ page = Math.min(Math.max(0, page + d), Math.max(0, Math.ceil(F.length/PER) - 1)); render(); window.scrollTo(0,0); }
document.getElementById('prev').onclick = document.getElementById('prev2').onclick = () => go(-1);
document.getElementById('next').onclick = document.getElementById('next2').onclick = () => go(1);
function racha(x){
  const d = (DELTAS[module] || {})[x.full_name] || 0;
  return d > 0 ? `<span class="bdg">🔥 +${fmt(d)} desde ${CORTES.anterior}</span>` : '';
}
function badges(x){
  const f = module === 'tre' ? x.created_at : x.pushed_at;
  const fl = module === 'tre' ? 'creado el ' : '';
  let extra = '';
  if (x.archived) extra += `<span class="bdg">⛔ archivado</span>`;
  if (esCopyleft(x.license)) extra += `<span class="bdg">⚠ copyleft</span>`;
  return `<span class="bdg">${x.language}</span><span class="bdg">${x.categoria}</span><span class="bdg">${x.license}</span><span class="bdg">${fmt(x.forks)} bifurcaciones</span><span class="bdg">${fl}${f}</span>${extra}<div class="mut" style="font-size:12px;margin-top:2px">${veredicto(x)}</div>`;
}
function prev(x, w){
  return `<a href="${x.url}" target="_blank" rel="noopener"><img class="prev" loading="lazy" alt="Vista previa de ${x.full_name}" src="https://opengraph.githubassets.com/1/${x.full_name}"></a>`;
}
function head(x){
  const tag = module === 'tre' ? `<span class="age">${age(x.created_at)}</span> ` : '';
  const k = module + '|' + x.full_name;
  const picked = !!FAV[k];
  return `<div>${tag}<strong>#${x.rank} ${x.full_name}</strong> &middot; <strong>${fmt(x.stars)} estrellas</strong> ${movBadge(x)} ${racha(x)}<div>${badges(x)}</div><p>${(x.descripcion_es||'Sin descripción')}</p><p class="mut"><em>Original:</em> ${(x.description||'')}</p><a href="${x.url}" target="_blank" rel="noopener">${x.url}</a><br><button class="pick${picked ? ' on' : ''}" data-m="${module}" data-n="${x.full_name}">${picked ? '★ Elegido' : '☆ Elegir'}</button></div>`;
}
document.getElementById('g').addEventListener('click', e => {
  const b = e.target.closest ? e.target.closest('.pick') : null;
  if (!b) return;
  const k = b.getAttribute('data-m') + '|' + b.getAttribute('data-n');
  if (FAV[k]) delete FAV[k]; else FAV[k] = 1;
  saveFav(); updateFavUI(); render();
});
function render(){
  const src = showFav ? favRows() : F;
  const pages = Math.max(1, Math.ceil(src.length / PER));
  page = Math.min(Math.max(0, page), pages - 1);
  const slice = src.slice(page * PER, page * PER + PER);
  document.getElementById('n').textContent = src.length + ' repositorios' + (showFav ? ' (elegidos)' : '');
  document.getElementById('p').textContent = document.getElementById('p2').textContent = 'Página ' + (page+1) + ' de ' + pages;
  updateFavUI();
  const dm = DELTAS[module] || {};
  const subs = F.filter(x => rankGain(x) > 0).sort((a, b) => (rankGain(b) - rankGain(a)) || ((dm[b.full_name] || 0) - (dm[a.full_name] || 0))).slice(0, 5);
  const caen = F.filter(x => rankGain(x) < 0 && rankGain(x) > -9999).sort((a, b) => rankGain(a) - rankGain(b)).slice(0, 3);
  const nuevos = F.filter(x => rankGain(x) === -9999);
  let movHtml = '';
  if (subs.length) movHtml += `<div class="card" style="margin-bottom:12px"><strong>🚀 Top subidas desde ${CORTES.anterior}:</strong> ` + subs.map(x => `<a href="${x.url}" target="_blank" rel="noopener">${x.full_name}</a> (▲${rankGain(x)} · +${fmt(dm[x.full_name] || 0)})`).join(' · ') + `</div>`;
  if (caen.length) movHtml += `<div class="card" style="margin-bottom:12px"><strong>📉 Caídas:</strong> ` + caen.map(x => `<a href="${x.url}" target="_blank" rel="noopener">${x.full_name}</a> (▼${-rankGain(x)})`).join(' · ') + `</div>`;
  if (nuevos.length) movHtml += `<div class="card" style="margin-bottom:12px"><strong>🆕 Nuevos en el ranking:</strong> ` + nuevos.slice(0, 8).map(x => `<a href="${x.url}" target="_blank" rel="noopener">${x.full_name}</a>`).join(' · ') + (nuevos.length > 8 ? ` · y ${nuevos.length - 8} más` : '') + `</div>`;
  document.getElementById('mov').innerHTML = movHtml;
  if (!slice.length){ g.innerHTML = showFav ? '<p class="mut">Aún no elegiste ninguno. Explora y pulsa ☆ Elegir en los que te gusten: se guardan en este navegador.</p>' : '<p class="mut">Sin repositorios con ese filtro. Amplía el rango o cambia la búsqueda.</p>'; return; }
  if (LAYOUT === 'table'){
    g.innerHTML = `<div class="card" style="overflow:auto;padding:0"><table><thead><tr><th scope="col">Puesto</th><th scope="col">Repositorio y qué hace</th><th scope="col">Estrellas</th><th scope="col">Vista previa</th></tr></thead><tbody>` +
      slice.map(x => `<tr><td class="num">${x.rank}</td><td>${head(x)}</td><td class="num"><strong>${fmt(x.stars)}</strong></td><td style="min-width:170px">${prev(x)}</td></tr>`).join('') + `</tbody></table></div>`;
  } else if (LAYOUT === 'split'){
    g.innerHTML = `<div class="grid">` + slice.map(x => `<div class="card" style="display:flex;gap:10px"><div style="flex:1;min-width:0">${head(x)}</div><div style="width:150px;flex-shrink:0">${prev(x)}</div></div>`).join('') + `</div>`;
  } else if (LAYOUT === 'bento'){
    const top = slice.slice(0, 6), rest = slice.slice(6);
    g.innerHTML = `<div class="grid3">` + top.map(x => `<div class="card" style="overflow:hidden;padding:0"><div>${prev(x)}</div><div style="padding:10px">${head(x)}</div></div>`).join('') + `</div><div class="grid" style="margin-top:12px">` + rest.map(x => `<div class="card" style="display:flex;gap:10px"><div style="flex:1;min-width:0">${head(x)}</div><div style="width:120px;flex-shrink:0">${prev(x)}</div></div>`).join('') + `</div>`;
  } else if (LAYOUT === 'list'){
    g.innerHTML = slice.map(x => `<div class="card" style="display:flex;gap:10px;margin-bottom:8px"><div style="flex:1;min-width:0">${head(x)}</div><div style="width:140px;flex-shrink:0">${prev(x)}</div></div>`).join('');
  } else if (LAYOUT === 'kanban'){
    const groups = {};
    slice.forEach(x => { (groups[x.categoria] = groups[x.categoria] || []).push(x); });
    g.innerHTML = `<div class="grid3">` + Object.keys(groups).sort().map(k => `<div><h3 class="colh">${k} (${groups[k].length})</h3>` + groups[k].map(x => `<div class="card" style="margin-bottom:8px">${head(x)}<div style="margin-top:6px">${prev(x)}</div></div>`).join('') + `</div>`).join('') + `</div>`;
  } else if (LAYOUT === 'podium'){
    const t3 = slice.slice(0, 3), rest = slice.slice(3);
    g.innerHTML = `<div class="grid3">` + t3.map((x, i) => `<div class="card" style="border:2px solid var(--acc)"><div class="medal mono">${['1','2','3'][i]}</div>${head(x)}<div style="margin-top:6px">${prev(x)}</div></div>`).join('') + `</div><div class="grid" style="margin-top:12px">` + rest.map(x => `<div class="card" style="display:flex;gap:10px"><div style="flex:1;min-width:0">${head(x)}</div><div style="width:120px;flex-shrink:0">${prev(x)}</div></div>`).join('') + `</div>`;
  } else {
    g.innerHTML = `<div class="grid">` + slice.map(x => `<div class="card">${head(x)}<div style="margin-top:8px">${prev(x)}</div></div>`).join('') + `</div>`;
  }
}
function fname(){ return module + '-github'; }
document.getElementById('bcsv').onclick = () => download('csv');
document.getElementById('bxlsx').onclick = () => download('xlsx');
document.getElementById('bjson').onclick = () => download('json');
document.getElementById('bpdf').onclick = () => download('pdf');
document.getElementById('bfav').onclick = () => { showFav = !showFav; page = 0; render(); };
document.getElementById('fcsv').onclick = () => download('csv', true);
document.getElementById('fxlsx').onclick = () => download('xlsx', true);
document.getElementById('fpdf').onclick = () => download('pdf', true);
document.getElementById('fclear').onclick = () => { FAV = {}; saveFav(); showFav = false; render(); };
function download(kind, onlyFav){
  const rows = onlyFav ? favRows() : F;
  if (onlyFav && !rows.length){ alert('Aún no elegiste ninguno. Pulsa ☆ Elegir primero.'); return; }
  const cambio = x => {
    for (const m of ['500', 'tre']){
      const pr = (RANKSPREV[m] || {})[x.full_name];
      if (pr !== undefined){
        const arr = m === '500' ? DB500 : DBTRE;
        const cur = arr.findIndex(y => y.full_name === x.full_name) + 1;
        return {g: pr - cur, d: (DELTAS[m] || {})[x.full_name] || 0};
      }
    }
    return {g: 0, d: 0};
  };
  if (kind === 'csv' || kind === 'json'){
    const txt = kind === 'json' ? JSON.stringify(rows, null, 1) :
      'puesto,nombre,estrellas,bifurcaciones,lenguaje,categoria,licencia,tipo,fecha,cambio_puestos,cambio_estrellas,url,descripcion,descripcion_original\\n' +
      rows.map(x => [x.rank, '"'+x.full_name+'"', x.stars, x.forks, x.language, x.categoria, x.license, x.tipo, x.created_at||x.pushed_at, cambio(x).g, cambio(x).d, x.url, '"'+(x.descripcion_es||'').replace(/"/g,'""')+'"', '"'+(x.description||'').replace(/"/g,'""')+'"'].join(',')).join('\\n');
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([txt], {type: kind === 'json' ? 'application/json' : 'text/csv'}));
    a.download = (onlyFav ? 'elegidos-' : '') + fname() + '.' + (kind === 'json' ? 'json' : 'csv'); a.click();
  } else if (kind === 'xlsx'){
    if (typeof XLSX === 'undefined'){ alert('Sin internet para el Excel filtrado. Usa el enlace de Excel completo.'); return; }
    const ws = XLSX.utils.json_to_sheet(rows.map(x => ({puesto:x.rank, nombre:x.full_name, descripcion:x.descripcion_es, descripcion_original:x.description, estrellas:x.stars, bifurcaciones:x.forks, lenguaje:x.language, categoria:x.categoria, licencia:x.license, tipo:x.tipo, fecha:x.created_at||x.pushed_at, cambio_puestos:cambio(x).g, cambio_estrellas:cambio(x).d, enlace:x.url})));
    const wb = XLSX.utils.book_new(); XLSX.utils.book_append_sheet(wb, ws, 'ranking');
    XLSX.writeFile(wb, (onlyFav ? 'elegidos-' : '') + fname() + '-filtrado.xlsx');
  } else if (kind === 'pdf'){
    const old = g.innerHTML;
    g.innerHTML = '<div class="card"><table><thead><tr><th>Puesto</th><th>Repositorio</th><th>Qué hace</th><th>Estrellas</th><th>Enlace</th></tr></thead><tbody>' +
      rows.map(x => `<tr><td>${x.rank}</td><td>${x.full_name}</td><td>${(x.descripcion_es||'').slice(0,200)}</td><td>${fmt(x.stars)}</td><td>${x.url}</td></tr>`).join('') + '</tbody></table></div>';
    window.print(); g.innerHTML = old; render();
  }
}
const MODES = [["01-signal-cards","Signal","#D63A2F"],["02-midnight-console","Consola","#4ADE80"],["04-ledger-table","Libro","#1D4ED8"],["05-tide-glass","Marea","#5EEAD4"],["07-control-tower","Torre","#4F46E5"],["08-atlas-kanban","Atlas","#0284C7"],["09-phosphor-terminal","Fósforo","#4ADE80"],["11-gallery-wall","Galería","#F59E0B"],["14-block-party","Bloque","#FF5C00"],["15-plum-material","Pluma","#7C3AED"],["16-cave-git","Cueva","#2F81F7"],["21-podium","Podio","#FBBF24"],["23-night-drive","Nocturna","#34D399"],["28-abyss","Abismo","#22D3EE"],["29-evergreen","Perenne","#4ADE80"],["30-ember","Brasa","#F97316"],["trending","Tendencias","#22D3EE"]];
(function(){
  const menu = document.getElementById('modomenu'), btn = document.getElementById('modobtn');
  const cur = "__FILE__";
  menu.innerHTML = MODES.map(m => `<a role="menuitem" data-f="${m[0]}" href="${m[0]}.html" class="${m[0] === cur ? 'cur' : ''}"><span>${m[0] === cur ? '● ' : ''}${m[1]}</span><span class="dot" style="background:${m[2]}"></span></a>`).join('');
  btn.onclick = e => { e.stopPropagation(); menu.classList.toggle('open'); };
  document.addEventListener('click', () => menu.classList.remove('open'));
  menu.addEventListener('click', e => {
    const a = e.target.closest ? e.target.closest('a') : null;
    if (!a) return;
    e.preventDefault();
    location.href = a.getAttribute('data-f') + '.html?mod=' + module;
  });
})();
const qmod = new URLSearchParams(location.search).get('mod');
setModule(qmod === 'tre' || qmod === '500' ? qmod : "__MODULE__");
ev('tema_visto', {tema: '__FILE__'});
</script>__UMAMI__</div></body></html>"""


PAL = {
"01-signal-cards": ("Archivo","Archivo","IBM Plex Mono","#FAFAF7","#FFFFFF","#16130E","#6B6257","#D63A2F","#FFFFFF","4px"),
"02-midnight-console": ("Sora","Sora","JetBrains Mono","#0A0E14","#11161F","#E6E1D8","#8A94A6","#4ADE80","#07130C","6px"),
"04-ledger-table": ("Roboto Slab","Roboto Slab","IBM Plex Mono","#FBFAF7","#FFFFFF","#1F1B16","#6E6259","#1D4ED8","#FFFFFF","2px"),
"05-tide-glass": ("Outfit","Outfit","Outfit","#0B1B26","rgba(255,255,255,.07)","#F2F7FA","#9DB4C0","#5EEAD4","#062A26","16px"),
"07-control-tower": ("DM Sans","DM Sans","JetBrains Mono","#F2F4FA","#FFFFFF","#141A2B","#5B6478","#4F46E5","#FFFFFF","10px"),
"08-atlas-kanban": ("Manrope","Manrope","Manrope","#F4F7FA","#FFFFFF","#10202E","#5B6B7B","#0277B6","#FFFFFF","12px"),
"09-phosphor-terminal": ("VT323","IBM Plex Mono","IBM Plex Mono","#041008","#06130B","#B6FFC9","#3E7A52","#4ADE80","#041008","0px"),
"11-gallery-wall": ("Sora","Hanken Grotesk","Hanken Grotesk","#141210","#1E1B17","#F5EFE4","#A89C88","#F59E0B","#231303","10px"),
"14-block-party": ("Archivo Black","Space Mono","Space Mono","#FFF3D6","#FFFFFF","#000000","#3D3D3D","#FF5C00","#1F0E00","0px"),
"15-plum-material": ("Figtree","Figtree","IBM Plex Mono","#F4EFFA","#FFFFFF","#221B2E","#6E6580","#7C3AED","#FFFFFF","16px"),
"16-cave-git": ("IBM Plex Mono","IBM Plex Mono","IBM Plex Mono","#0D1117","#161B22","#E6EDF3","#8B949E","#1F6FEB","#FFFFFF","6px"),
"21-podium": ("Oswald","Cabin","Cabin","#101828","#1A2436","#F8F3E7","#9AA3B2","#FBBF24","#231603","8px"),
"23-night-drive": ("Sora","Sora","JetBrains Mono","#08090D","#101218","#EDEFF5","#8E93A3","#34D399","#05281C","14px"),
"28-abyss": ("Chakra Petch","Chakra Petch","IBM Plex Mono","#041E2E","#07293D","#E8F6FF","#7FA8BE","#22D3EE","#06252B","4px"),
"29-evergreen": ("Bitter","Work Sans","Work Sans","#0A1F14","#10281A","#E9F5EC","#8FB69C","#4ADE80","#05281A","12px"),
"30-ember": ("DM Serif Display","Karla","Karla","#1A0E08","#241209","#FBF3E8","#C0A488","#F97316","#261000","6px"),
"trending": ("Sora","Sora","JetBrains Mono","#070B14","#111A2E","#E8ECF5","#9AA7C2","#22D3EE","#070B14","12px"),
}
def fontlink(disp, body, mono):
    fams = []
    for f in (disp, body, mono):
        if f not in fams:
            fams.append(f)
    q = "&".join("family=" + f.replace(" ", "+") + ":wght@400;600;700" for f in fams)
    return "<link href='https://fonts.googleapis.com/css2?" + q + "&display=swap' rel='stylesheet'>"

for (fid, title, layout, css, hero) in FILES:
    mod = "tre" if fid == "trending" else "500"
    html = TPL.replace("__TITLE__", title).replace("__LAYOUT__", layout)
    html = html.replace("__EXTRA_CSS__", css).replace("__EXTRA_HERO__", hero)
    html = html.replace("__MODULE__", mod).replace("__DB500__", TOP).replace("__DBTRE__", TRE).replace("__FILE__", fid)
    html = html.replace("__DELTAS__", DELTAS).replace("__SERIES__", SERIES).replace("__CORTES__", CORTES).replace("__RANKSPREV__", RANKSPREV)
    html = html.replace("__HOY__", HOY).replace("__DMIN__", DMIN).replace("__FCORTE__", FCORTE)
    html = html.replace("__UMAMI__", UMAMI)
    html = html.replace("__DESC__", "Ranking GitHub en español con el tema %s: los 500 repos con más estrellas y 200 tendencias, filtros y descargas." % title)
    html = html.replace("__CANON__", ('<link rel="canonical" href="%s/%s.html">\n<meta property="og:url" content="%s/%s.html">' % (SITEURL, fid, SITEURL, fid)) if SITEURL else "")
    disp, body, mono, bg, card, ink, mut, acc, acctext, rad = PAL[fid]
    html = html.replace("__FONTLINK__", fontlink(disp, body, mono))
    html = html.replace("__DISP__", disp).replace("__BODY__", body).replace("__MONO__", mono)
    html = html.replace("__BG__", bg).replace("__CARD__", card).replace("__INK__", ink)
    html = html.replace("__MUT__", mut).replace("__ACC__", acc).replace("__ACCTEXT__", acctext).replace("__RAD__", rad)
    open(os.path.join(SRC, fid + ".html"), "w", encoding="utf-8").write(html)
    print(fid, len(html) // 1024, "KB")
