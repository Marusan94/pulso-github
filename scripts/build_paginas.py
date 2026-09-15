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


def series(kind, current):
    por_repo = {}
    for s in sorted(glob.glob(os.path.join(DATA, "history", "*-" + kind + ".json"))):
        d = json.load(open(s, encoding="utf-8"))
        for r in d["repos"]:
            por_repo.setdefault(r["n"], []).append([d["fecha"], r["s"]])
    for x in current["repos"]:
        lst = por_repo.setdefault(x["full_name"], [])
        if not lst or lst[-1][0] != current.get("fecha", ""):
            lst.append([current.get("fecha", ""), x["stars"]])
    return por_repo


SERIES = json.dumps({"500": series("top", TOP_DATA), "tre": series("tre", TRE_DATA)}, ensure_ascii=False)

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
<nav class="tabs noprint"><a href="analiticas.html" id="t-ana">◔ Analytics</a><a href="noticias.html" id="t-not">📰 Noticias</a><a href="29-evergreen.html">⌂ Inicio</a></nav>
__BODY__
</div>
<script>
const DB500 = __DB500__;
const DBTRE = __DBTRE__;
const DELTAS = __DELTAS__;
const SERIES = __SERIES__;
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
<div class="card"><h3>Curva del ranking <small class="mut">— pasa el cursor para previsualizar</small></h3>
<div class="seg" role="group" aria-label="Tipo de curva" style="max-width:420px"><button id="cRank" class="on">Ranking actual</button><button id="cTime">En el tiempo</button></div>
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
  dibujaCurva();
  dibujaRadar();
}
let curvaModo = 'rank';
document.getElementById('cRank').onclick = () => { curvaModo = 'rank'; document.getElementById('cRank').classList.add('on'); document.getElementById('cTime').classList.remove('on'); dibujaCurva(); };
document.getElementById('cTime').onclick = () => { curvaModo = 'time'; document.getElementById('cTime').classList.add('on'); document.getElementById('cRank').classList.remove('on'); dibujaCurva(); };
function dibujaCurva(){
  const svg = document.getElementById('chart'), tip = document.getElementById('tip'), note = document.getElementById('chartnote');
  const W = 960, H = 340, P = 46;
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
  const D = DB().slice().sort((a, b) => b.stars - a.stars).slice(0, 30);
  const lvs = D.map(x => Math.log10(Math.max(1, x.stars)));
  const mn = Math.min(...lvs), mx = Math.max(...lvs), rg = (mx - mn) || 1;
  const X = i => P + i * (W - 2 * P) / (D.length - 1);
  const Y = v => H - P - (v - mn) / rg * (H - 2 * P);
  const pts = D.map((x, i) => `${X(i).toFixed(1)},${Y(lvs[i]).toFixed(1)}`).join(' ');
  let h = `<defs><linearGradient id="gg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${acc}" stop-opacity=".4"/><stop offset="1" stop-color="${acc}" stop-opacity="0"/></linearGradient></defs>`;
  h += `<polygon points="${P},${H - P} ${pts} ${W - P},${H - P}" fill="url(#gg)"/>`;
  h += `<polyline points="${pts}" fill="none" stroke="${acc}" stroke-width="2.5"/>`;
  [0, 1, 2].forEach(j => {
    const v = mn + rg * j / 2, y = Y(v);
    h += `<line x1="${P}" y1="${y}" x2="${W - P}" y2="${y}" stroke="currentColor" opacity=".15"/><text x="${P - 6}" y="${y + 5}" fill="currentColor" font-size="14" text-anchor="end" opacity=".6">${fmt(Math.round(Math.pow(10, v)))}</text>`;
  });
  h += D.map((x, i) => `<circle cx="${X(i).toFixed(1)}" cy="${Y(lvs[i]).toFixed(1)}" r="4.5" fill="var(--card, #10281A)" stroke="${acc}" stroke-width="2.5" style="pointer-events:none"/>`).join('');
  h += D.slice(0, 5).map((x, i) => `<text x="${X(i).toFixed(1)}" y="${(Y(lvs[i]) - 10).toFixed(1)}" fill="currentColor" font-size="15" font-weight="800" text-anchor="middle">#${x.rank}</text>`).join('');
  h += D.map((x, i) => `<circle data-i="${i}" cx="${X(i).toFixed(1)}" cy="${Y(lvs[i]).toFixed(1)}" r="11" fill="transparent"/>`).join('');
  svg.innerHTML = h;
  note.textContent = 'Top 30 del módulo en escala logarítmica, como una gráfica de trading: cae rápido y la cola es larga.';
  document.getElementById('chartlegend').textContent = `Viendo ${D.length} repos de ${module === '500' ? 'Los 500' : 'Tendencias'} · líder ${D[0].full_name} con ${fmt(D[0].stars)} estrellas · corte ${CORTE || HOY}.`;
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
    h = h.replace("__DELTAS__", DELTAS).replace("__SERIES__", SERIES).replace("__CORTE__", CORTE)
    open(os.path.join(SITE, nombre), "w", encoding="utf-8").write(h)
    print(nombre, len(h) // 1024, "KB")


pagina("analiticas.html", "Analytics", "Reparto por categoría, lenguaje y licencias del ranking.", "500", ANA_BODY, ANA_JS)
pagina("noticias.html", "Noticias", "Titulares generados del ranking: novedades, hitos y rachas.", "tre", NOT_BODY, NOT_JS)
