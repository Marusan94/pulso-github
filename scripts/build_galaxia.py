"""Genera docs/galaxia.html - Galaxia 3D del Ranking (autonoma, datos embebidos).

Uso:
    python scripts/build_galaxia.py
Lee data/repos.json (top 500) y data/trending.json, los compacta y los
inyecta en el template. La pagina resultante funciona con doble clic
(file://) y desplegada (Netlify), sin llamadas a APIs externas.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SITE = os.path.join(ROOT, "docs")

UMAMI_URL = (os.environ.get("UMAMI_URL") or "").strip()
UMAMI_ID = (os.environ.get("UMAMI_ID") or "").strip()
UMAMI = ('<script defer src="%s" data-website-id="%s"></script>' % (UMAMI_URL, UMAMI_ID)) if (UMAMI_URL and UMAMI_ID) else ""


def compact(repos):
    out = []
    for r in repos:
        fn = r.get("full_name", "")
        name = r.get("name") or (fn.split("/")[-1] if "/" in fn else fn)
        desc = (r.get("descripcion_es") or r.get("description") or "")[:150]
        lang = r.get("language") or "Otro"
        url = r.get("url") or ("https://github.com/" + fn)
        out.append([r.get("rank", 0), fn, name, r.get("stars", 0),
                    r.get("forks", 0), lang, r.get("categoria") or "Otros",
                    desc, url, (r.get("pushed_at") or "")[:10]])
    return out


top = json.load(open(os.path.join(DATA, "repos.json"), encoding="utf-8"))
tre = json.load(open(os.path.join(DATA, "trending.json"), encoding="utf-8"))

payload = {
    "fecha_top": top.get("fecha", ""),
    "fecha_tre": tre.get("fecha", ""),
    "ventana": tre.get("ventana", ""),
    "top": compact(top["repos"]),
    "tre": compact(tre["repos"]),
}
DATA_JS = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))

TEMPLATE = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Galaxia 3D &middot; Ranking GitHub</title>
<meta name="description" content="Galaxia 3D interactiva: los 500 repos con mas estrellas y 200 tendencias, agrupados por categoria.">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
__UMAMI__
<style>
html,body{margin:0;padding:0;height:100%;overflow:hidden;background:#05070f;color:#e6edf3;font-family:'Segoe UI',system-ui,sans-serif}
#scene{position:fixed;inset:0;display:block}
.nav{position:fixed;top:14px;left:16px;z-index:20;display:flex;gap:8px;flex-wrap:wrap}
.nav a{color:#5eead4;text-decoration:none;font-size:.85rem;background:rgba(10,15,25,.72);border:1px solid #1e2a3a;padding:7px 12px;border-radius:8px;backdrop-filter:blur(8px)}
.nav a.on{background:#0d3b34;border-color:#5eead4}
.hud{position:fixed;top:64px;left:16px;z-index:20;background:rgba(8,12,20,.78);border:1px solid #1e2a3a;border-radius:12px;padding:14px 16px;backdrop-filter:blur(10px);max-width:300px}
.hud h1{margin:0 0 2px;font-size:1.15rem;letter-spacing:.3px}
.hud h1 .g{background:linear-gradient(135deg,#5eead4,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent}
.hud p{margin:4px 0;font-size:.8rem;color:#9aa7b8}
.hud .row{display:flex;justify-content:space-between;font-size:.8rem;margin-top:6px}
.hud .row b{color:#fff;font-variant-numeric:tabular-nums}
.panel{position:fixed;top:14px;right:16px;z-index:20;width:288px;background:rgba(8,12,20,.82);border:1px solid #1e2a3a;border-radius:12px;padding:14px 16px;backdrop-filter:blur(10px);font-size:.82rem}
.panel h3{margin:0 0 8px;font-size:.85rem;color:#9aa7b8;text-transform:uppercase;letter-spacing:.6px}
.panel input[type=text]{width:100%;box-sizing:border-box;background:#0b1220;border:1px solid #263349;color:#e6edf3;border-radius:8px;padding:8px 10px;font-size:.85rem;margin-bottom:8px}
.panel select{width:100%;background:#0b1220;border:1px solid #263349;color:#e6edf3;border-radius:8px;padding:7px;margin:4px 0 8px;font-size:.82rem}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 10px}
.chip{font-size:.72rem;padding:4px 9px;border-radius:999px;border:1px solid #2b3a52;color:#9aa7b8;cursor:pointer;user-select:none}
.chip.off{opacity:.35}
.chip b{font-weight:700}
.sld{margin:6px 0}
.sld label{display:flex;justify-content:space-between;color:#9aa7b8;font-size:.75rem;margin-bottom:2px}
.sld input{width:100%}
.btns{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.btn{font-size:.75rem;padding:6px 10px;border-radius:8px;border:1px solid #2b3a52;background:#0e1626;color:#c8d3e0;cursor:pointer}
.btn.on{background:#0d3b34;border-color:#5eead4;color:#5eead4}
.modes{display:flex;gap:6px;margin-bottom:10px}
.mode{flex:1;text-align:center;font-size:.78rem;padding:7px 0;border-radius:8px;border:1px solid #2b3a52;background:#0e1626;color:#c8d3e0;cursor:pointer}
.mode.on{background:#13283f;border-color:#7aa2f7;color:#fff}
.card{position:fixed;right:16px;bottom:16px;z-index:20;width:320px;max-width:calc(100vw - 32px);background:rgba(8,12,20,.92);border:1px solid #2b3a52;border-radius:12px;padding:14px 16px;backdrop-filter:blur(10px);display:none;font-size:.82rem}
.card.show{display:block}
.card h2{margin:0 0 2px;font-size:1rem;word-break:break-word}
.card h2 .rk{color:#fbbf24;font-weight:800;margin-right:6px}
.card .meta{display:flex;gap:10px;flex-wrap:wrap;color:#9aa7b8;font-size:.76rem;margin:6px 0}
.card .meta i{margin-right:4px}
.card p.desc{color:#c8d3e0;font-size:.8rem;line-height:1.45;margin:8px 0}
.card a.go{display:inline-block;margin-top:4px;color:#05070f;background:#5eead4;font-weight:700;text-decoration:none;padding:7px 14px;border-radius:8px;font-size:.8rem}
.card a.sim{color:#5eead4;font-size:.76rem;margin-left:12px;cursor:pointer}
.langdot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px}
.legend{position:fixed;left:16px;bottom:16px;z-index:20;background:rgba(8,12,20,.78);border:1px solid #1e2a3a;border-radius:12px;padding:10px 14px;backdrop-filter:blur(10px);font-size:.74rem;color:#9aa7b8;max-width:300px}
.legend div{margin:3px 0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#tip{position:fixed;z-index:30;pointer-events:none;background:rgba(5,8,15,.92);border:1px solid #2b3a52;border-radius:8px;padding:6px 10px;font-size:.75rem;display:none;max-width:240px}
#tip b{color:#fff}
#tip span{color:#fbbf24}
#err{position:fixed;inset:0;display:none;place-items:center;z-index:50;background:#05070f;color:#e6edf3;text-align:center;padding:24px}
.phead{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:6px}
.phead .t{font-size:.78rem;color:#9aa7b8;text-transform:uppercase;letter-spacing:.6px;font-weight:700}
.minbtn{flex:0 0 auto;width:22px;height:22px;border-radius:6px;border:1px solid #2b3a52;background:#0e1626;color:#9aa7b8;cursor:pointer;font-size:.72rem;line-height:1;padding:0}
.minbtn:hover{color:#fff;border-color:#5eead4}
.min .cbody{display:none}
.min{padding-bottom:10px}
body.uihidden .hud,body.uihidden .panel,body.uihidden .legend,body.uihidden .card,body.uihidden .nav{display:none}
.mapctl{position:fixed;right:16px;top:50%;transform:translateY(-50%);z-index:20;display:flex;flex-direction:column;gap:6px}
.mapctl button{width:38px;height:38px;border-radius:10px;border:1px solid #2b3a52;background:rgba(8,12,20,.85);color:#e6edf3;font-size:1rem;cursor:pointer;backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;padding:0}
.mapctl button:hover{border-color:#5eead4;color:#5eead4}
.mapctl button.on{border-color:#5eead4;color:#5eead4}
.mapctl .needle{transition:transform .1s linear;display:inline-block}
@media(max-width:900px){.hud{display:none}.panel{width:230px}.legend{display:none}.mapctl{right:8px}.mapctl button{width:34px;height:34px}}
</style>
<script type="importmap">{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}</script>
</head><body>
<canvas id="scene"></canvas>
<nav class="nav"><a href="index.html"><i class="fas fa-arrow-left"></i> Volver</a></nav>
<div class="hud" id="hud"><div class="phead"><span class="t">Galaxia del Ranking</span><button class="minbtn" data-min="hud" title="Minimizar">—</button></div><div class="cbody"><h1 style="margin:0 0 2px;font-size:1.15rem"><span class="g">Galaxia</span> del Ranking</h1><p id="fecha">500 repos &middot; corte —</p><div class="row"><span>Visibles</span><b id="stVis">0 / 0</b></div><div class="row"><span>Conexiones</span><b id="stEdge">0</b></div><div class="row"><span>FPS</span><b id="stFps">—</b></div><p style="margin-top:8px">Clic en una esfera para su ficha &middot; doble clic para volar &middot; arrastra para orbitar.</p></div></div>
<div class="panel" id="panel"><div class="phead"><span class="t">Controles</span><button class="minbtn" data-min="panel" title="Minimizar">—</button></div><div class="cbody"><h3>Conjuntos</h3><div class="modes"><div class="mode on" id="mTop">Top 500</div><div class="mode" id="mTre">Trending</div></div><h3>Buscar repo</h3><input type="text" id="q" placeholder="ej: rust, langchain, neovim…" list="dl"><datalist id="dl"></datalist><h3>Categorias</h3><div class="chips" id="chips"></div><h3>Lenguaje</h3><select id="lang"><option value="">Todos</option></select><div class="sld"><label><span>Min. estrellas</span><b id="vStars">0</b></label><input type="range" id="minStars" min="0" max="550000" step="5000" value="0"></div><div class="sld"><label><span>Solo top N</span><b id="vTop">500</b></label><input type="range" id="topN" min="10" max="500" step="10" value="500"></div><div class="btns"><button class="btn on" id="bEdge">Conexiones: on</button><button class="btn on" id="bRot">Rotacion: on</button><button class="btn on" id="bLab">Etiquetas: on</button><button class="btn" id="bReset">Reset vista</button></div></div></div>
<div class="mapctl" id="mapctl"><button id="zin" title="Acercar (+)"><i class="fas fa-plus"></i></button><button id="zout" title="Alejar (−)"><i class="fas fa-minus"></i></button><button id="zhome" title="Vista inicial (0)"><i class="fas fa-house"></i></button><button id="znorth" title="Orientar al norte (N)"><span class="needle" id="needle">🧭</span></button><button id="zfull" title="Pantalla completa (F)"><i class="fas fa-expand"></i></button><button id="zui" class="on" title="Mostrar/ocultar paneles (H)"><i class="fas fa-eye"></i></button></div>
<div class="card" id="card"><div class="phead"><span class="t">Ficha del repo</span><button class="minbtn" id="cardX" title="Cerrar">✕</button></div><div class="cbody"><h2><span class="rk" id="cRank">#1</span><span id="cName">—</span></h2><div class="meta"><span id="cStars">★ 0</span><span id="cForks">⑂ 0</span><span id="cLang">—</span><span id="cCat">—</span></div><p class="desc" id="cDesc"></p><div><a class="go" id="cUrl" href="#" target="_blank" rel="noopener">Abrir en GitHub ↗</a><a class="sim" id="cSim">ver similar →</a></div></div></div>
<div class="legend" id="legendWrap"><div class="phead"><span class="t">Lenguajes</span><button class="minbtn" data-min="legendWrap" title="Minimizar">—</button></div><div class="cbody" id="legend"></div></div>
<div id="tip"></div>
<div id="err"><div><h2>Tu navegador no soporta WebGL</h2><p>Abre esta pagina en Chrome, Edge, Firefox o Safari actualizado.</p></div></div>
<script>
const GALAXIA_DATA = __GALAXIA_JSON__;
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const F = { RANK: 0, FULL: 1, NAME: 2, STARS: 3, FORKS: 4, LANG: 5, CAT: 6, DESC: 7, URL: 8, PUSHED: 9 };
const LANG_COLORS = { Python: '#3572A5', TypeScript: '#3178c6', JavaScript: '#f1e05a', Go: '#00ADD8', Rust: '#dea584', 'C++': '#f34b7d', Java: '#b07219', Shell: '#89e051', 'Jupyter Notebook': '#DA5B0B', C: '#555555', Ruby: '#701516', HTML: '#e34c26', CSS: '#563d7c', 'C#': '#178600', PHP: '#4F5D95', Swift: '#F05138', Kotlin: '#A97BFF', Dart: '#00B4AB', Lua: '#000080', R: '#198CE7', Scala: '#c22d40', Vue: '#41b883', Svelte: '#ff3e00', Zig: '#ec915c', Markdown: '#083fa1', PowerShell: '#012456', Dockerfile: '#384d54', TeX: '#3D6117', GDScript: '#355570', Nix: '#7e7fff', Perl: '#0298c3', Julia: '#a270ba', Elixir: '#6e4a7e', Haskell: '#5e5086' };
const FALLBACK = '#8b949e';
const langColor = l => LANG_COLORS[l] || FALLBACK;
const langNorm = l => (l && LANG_COLORS[l]) ? l : 'Otro';
const fmt = n => n >= 1e6 ? (n / 1e6).toFixed(1) + 'M' : n >= 1e3 ? (n / 1e3).toFixed(1) + 'k' : '' + n;
const mulberry = a => () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
const $ = id => document.getElementById(id);
const state = { mode: 'top', repos: [], pos: [], base: [], size: [], phase: [], vis: [], edges: [], showEdge: true, labels: true, selected: -1, hover: -1, tween: null };
const canvas = $('scene');
let renderer;
try {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
} catch (e) { $('err').style.display = 'grid'; throw e; }
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setClearColor(0x05070f, 1);
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x05070f, 0.00075);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 1, 4000);
const CAM0 = new THREE.Vector3(0, 210, 580);
camera.position.copy(CAM0);
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true; controls.dampingFactor = 0.06;
controls.minDistance = 25; controls.maxDistance = 1400;
controls.autoRotate = true; controls.autoRotateSpeed = 0.25;
scene.add(new THREE.AmbientLight(0xffffff, 0.55));
const d1 = new THREE.DirectionalLight(0x9fd8ff, 1.0); d1.position.set(200, 300, 200); scene.add(d1);
const d2 = new THREE.DirectionalLight(0xa78bfa, 0.45); d2.position.set(-250, 80, -200); scene.add(d2);
const galaxy = new THREE.Group(); scene.add(galaxy);
const grid = new THREE.PolarGridHelper(430, 12, 7, 72, 0x1b2940, 0x111b2e);
grid.position.y = -70; grid.material.transparent = true; grid.material.opacity = 0.5; scene.add(grid);
const starGeo = new THREE.BufferGeometry();
{
  const N = 1400, p = new Float32Array(N * 3), c = new Float32Array(N * 3), rnd = mulberry(7);
  const pal = [[0.62, 0.85, 1], [0.66, 0.55, 0.98], [1, 1, 1], [0.37, 0.92, 0.83]];
  for (let i = 0; i < N; i++) {
    const r = 700 + rnd() * 900, th = rnd() * Math.PI * 2, ph = Math.acos(2 * rnd() - 1);
    p[i * 3] = r * Math.sin(ph) * Math.cos(th); p[i * 3 + 1] = r * Math.cos(ph) * 0.7; p[i * 3 + 2] = r * Math.sin(ph) * Math.sin(th);
    const cc = pal[(rnd() * pal.length) | 0], b = 0.35 + rnd() * 0.65;
    c[i * 3] = cc[0] * b; c[i * 3 + 1] = cc[1] * b; c[i * 3 + 2] = cc[2] * b;
  }
  starGeo.setAttribute('position', new THREE.BufferAttribute(p, 3));
  starGeo.setAttribute('color', new THREE.BufferAttribute(c, 3));
}
const stars = new THREE.Points(starGeo, new THREE.PointsMaterial({ size: 2.2, vertexColors: true, transparent: true, opacity: 0.85, sizeAttenuation: true, depthWrite: false }));
scene.add(stars);
const sphereGeo = new THREE.SphereGeometry(1, 20, 20);
let nodeMesh = null, glowMesh = null, edgeLines = null, hiLines = null, labelGroup = null, selRing = null, hoverTag = null;
let hoverTagId = -1;
const dummy = new THREE.Object3D();
const tmpColor = new THREE.Color();
function textSprite(text, px, fg, bg, pad) {
  const cv = document.createElement('canvas'), cx = cv.getContext('2d');
  cx.font = '700 ' + px + 'px Segoe UI, system-ui, sans-serif';
  const w = Math.ceil(cx.measureText(text).width) + pad * 2;
  cv.width = w; cv.height = px + pad * 2;
  const c2 = cv.getContext('2d');
  if (bg) { c2.fillStyle = bg; if (c2.roundRect) { c2.beginPath(); c2.roundRect(0, 0, cv.width, cv.height, 10); c2.fill(); } else c2.fillRect(0, 0, cv.width, cv.height); }
  c2.font = '700 ' + px + 'px Segoe UI, system-ui, sans-serif';
  c2.fillStyle = fg; c2.textBaseline = 'middle'; c2.fillText(text, pad, cv.height / 2 + 1);
  const tx = new THREE.CanvasTexture(cv); tx.colorSpace = THREE.SRGBColorSpace;
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: tx, transparent: true, depthWrite: false }));
  sp.scale.set(cv.width / 4, cv.height / 4, 1);
  return sp;
}
function clearGalaxy() {
  for (const o of [nodeMesh, glowMesh, edgeLines, hiLines, labelGroup, selRing, hoverTag]) {
    if (!o) continue;
    galaxy.remove(o); scene.remove(o);
    o.traverse(n => {
      if (n.geometry && n.geometry !== sphereGeo && n.geometry !== starGeo) n.geometry.dispose();
      if (n.material) { (Array.isArray(n.material) ? n.material : [n.material]).forEach(m => { if (m.map) m.map.dispose(); m.dispose(); }); }
    });
  }
  nodeMesh = glowMesh = edgeLines = hiLines = labelGroup = selRing = hoverTag = null;
  hoverTagId = -1;
}
function layout(repos) {
  const cats = {};
  repos.forEach((r, i) => { (cats[r[F.CAT]] = cats[r[F.CAT]] || []).push(i); });
  const names = Object.keys(cats).sort((a, b) => cats[b].length - cats[a].length);
  const R = 250, out = new Array(repos.length);
  const centers = {};
  names.forEach((cn, ci) => {
    const a = (ci / names.length) * Math.PI * 2 - Math.PI / 2;
    centers[cn] = { x: Math.cos(a) * R, y: ((ci % 3) - 1) * 40, z: Math.sin(a) * R, list: cats[cn], name: cn };
  });
  const GA = Math.PI * (3 - Math.sqrt(5));
  names.forEach(cn => {
    const c = centers[cn], rnd = mulberry(cn.length * 977 + 13);
    c.list.forEach((ri, k) => {
      const rr = 7 + 8.5 * Math.sqrt(k), th = k * GA;
      out[ri] = { x: c.x + Math.cos(th) * rr, y: c.y + (rnd() - 0.5) * 12, z: c.z + Math.sin(th) * rr, cx: c.x, cy: c.y, cz: c.z };
    });
  });
  return { out, centers, names };
}
function buildEdges(repos) {
  const groups = {};
  repos.forEach((r, i) => {
    const k = r[F.CAT] + '|' + langNorm(r[F.LANG]);
    (groups[k] = groups[k] || []).push(i);
  });
  const edges = [];
  Object.values(groups).forEach(g => {
    g.sort((a, b) => repos[b][F.STARS] - repos[a][F.STARS]);
    for (let i = 0; i + 1 < g.length; i++) edges.push([g[i + 1], g[i]]);
  });
  return edges;
}
function buildGalaxy() {
  clearGalaxy();
  const src = state.mode === 'top' ? GALAXIA_DATA.top : GALAXIA_DATA.tre;
  state.repos = src;
  const n = src.length;
  const { out, centers, names } = layout(src);
  state.pos = out; state.centers = centers; state.catNames = names;
  let mn = Infinity, mx = 0;
  src.forEach(r => { const s = Math.log10(r[F.STARS] + 1); if (s < mn) mn = s; if (s > mx) mx = s; });
  state.base = new Array(n); state.size = new Array(n); state.phase = new Array(n); state.vis = new Array(n).fill(true);
  nodeMesh = new THREE.InstancedMesh(sphereGeo, new THREE.MeshStandardMaterial({ roughness: 0.32, metalness: 0.15 }), n);
  glowMesh = new THREE.InstancedMesh(sphereGeo, new THREE.MeshBasicMaterial({ transparent: true, opacity: 0.16, blending: THREE.AdditiveBlending, depthWrite: false }), n);
  for (let i = 0; i < n; i++) {
    const r = src[i], t = (Math.log10(r[F.STARS] + 1) - mn) / Math.max(1e-6, mx - mn);
    const s = 1.5 + 3.8 * t;
    state.size[i] = s; state.base[i] = out[i]; state.phase[i] = (i * 0.7) % (Math.PI * 2);
    tmpColor.set(langColor(langNorm(r[F.LANG])));
    nodeMesh.setColorAt(i, tmpColor); glowMesh.setColorAt(i, tmpColor);
  }
  nodeMesh.instanceColor.needsUpdate = true; glowMesh.instanceColor.needsUpdate = true;
  nodeMesh.userData.isNodes = true;
  galaxy.add(nodeMesh); galaxy.add(glowMesh);
  state.edges = buildEdges(src);
  const ep = new Float32Array(state.edges.length * 6);
  edgeLines = new THREE.LineSegments(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({ color: 0x5eead4, transparent: true, opacity: 0.10 }));
  edgeLines.geometry.setAttribute('position', new THREE.BufferAttribute(ep, 3));
  edgeLines.visible = state.showEdge; galaxy.add(edgeLines);
  hiLines = new THREE.LineSegments(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({ color: 0x5eead4, transparent: true, opacity: 0.9 }));
  hiLines.geometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array(12 * 6), 3));
  hiLines.visible = false; galaxy.add(hiLines);
  labelGroup = new THREE.Group(); galaxy.add(labelGroup);
  names.forEach(cn => {
    const c = centers[cn];
    const sp = textSprite(cn + ' · ' + c.list.length, 30, '#cfe3ff', 'rgba(10,18,32,.78)', 18);
    sp.position.set(c.x, c.y + 8.5 * Math.sqrt(c.list.length) + 22, c.z);
    sp.userData.isCat = true; labelGroup.add(sp);
  });
  src.forEach((r, i) => {
    if (r[F.RANK] > 10 || r[F.RANK] < 1) return;
    const sp = textSprite('#' + r[F.RANK] + ' ' + r[F.NAME], 26, '#ffd97a', 'rgba(20,14,4,.82)', 14);
    sp.position.set(out[i].x, out[i].y + state.size[i] + 9, out[i].z);
    sp.userData.repo = i; labelGroup.add(sp);
  });
  selRing = new THREE.Mesh(new THREE.TorusGeometry(1, 0.07, 10, 48), new THREE.MeshBasicMaterial({ color: 0xfbbf24, transparent: true, opacity: 0.95 }));
  selRing.visible = false; scene.add(selRing);
  hoverTag = new THREE.Sprite(new THREE.SpriteMaterial({ transparent: true, depthWrite: false, depthTest: false }));
  hoverTag.visible = false; hoverTag.renderOrder = 5; galaxy.add(hoverTag);
  refreshEdges(); applyFilters(); buildFilterUI();
}
function refreshEdges() {
  if (!edgeLines) return;
  const attr = edgeLines.geometry.getAttribute('position');
  let k = 0;
  for (const [a, b] of state.edges) {
    if (!state.vis[a] || !state.vis[b]) continue;
    const A = state.pos[a], B = state.pos[b];
    attr.array[k++] = A.x; attr.array[k++] = A.y; attr.array[k++] = A.z;
    attr.array[k++] = B.x; attr.array[k++] = B.y; attr.array[k++] = B.z;
  }
  edgeLines.geometry.setDrawRange(0, k / 3);
  attr.needsUpdate = true;
  $('stEdge').textContent = state.showEdge ? (k / 6) + ' visibles' : state.edges.length + ' (off)';
}
function applyFilters() {
  const lang = $('lang').value, minS = +$('minStars').value, topN = +$('topN').value;
  const offCats = new Set([...document.querySelectorAll('#chips .chip.off')].map(c => c.dataset.cat));
  let vis = 0;
  state.repos.forEach((r, i) => {
    const ok = !offCats.has(r[F.CAT]) && (!lang || langNorm(r[F.LANG]) === lang) && r[F.STARS] >= minS && r[F.RANK] >= 1 && r[F.RANK] <= topN;
    state.vis[i] = ok; if (ok) vis++;
  });
  if (state.selected >= 0 && !state.vis[state.selected]) select(-1);
  $('stVis').textContent = vis + ' / ' + state.repos.length;
  $('vStars').textContent = fmt(minS); $('vTop').textContent = topN;
  refreshEdges(); refreshHi();
}
function buildFilterUI() {
  const chips = $('chips'); chips.innerHTML = '';
  state.catNames.forEach(cn => {
    const n = state.centers[cn].list.length;
    const d = document.createElement('div');
    d.className = 'chip'; d.dataset.cat = cn; d.innerHTML = '<b>' + cn + '</b> ' + n;
    d.onclick = () => { d.classList.toggle('off'); applyFilters(); };
    chips.appendChild(d);
  });
  const sel = $('lang'), langs = [...new Set(state.repos.map(r => langNorm(r[F.LANG])))].sort();
  const cur = sel.value; sel.innerHTML = '<option value="">Todos</option>';
  const counts = {};
  state.repos.forEach(r => { const l = langNorm(r[F.LANG]); counts[l] = (counts[l] || 0) + 1; });
  langs.forEach(l => {
    const o = document.createElement('option'); o.value = l;
    o.textContent = l + ' (' + counts[l] + ')';
    sel.appendChild(o);
  });
  if ([...sel.options].some(o => o.value === cur)) sel.value = cur;
  const lg = $('legend');
  const top = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 8);
  lg.innerHTML = '<b style="color:#e6edf3">Lenguajes top</b>' + top.map(([l, c]) => '<div><span class="langdot" style="background:' + langColor(l) + '"></span>' + l + ' · ' + c + '</div>').join('');
  const dl = $('dl'); dl.innerHTML = '';
  state.repos.forEach((r, i) => {
    if (i % 1 === 0) { const o = document.createElement('option'); o.value = r[F.FULL]; dl.appendChild(o); }
  });
  const maxS = Math.max(...state.repos.map(r => r[F.STARS]));
  $('minStars').max = Math.ceil(maxS / 10000) * 10000;
  const maxR = Math.max(...state.repos.map(r => r[F.RANK]));
  const tn = $('topN'); tn.max = maxR; tn.value = maxR;
  $('fecha').innerHTML = (state.mode === 'top' ? state.repos.length + ' repos' : state.repos.length + ' tendencias') + ' &middot; corte ' + (state.mode === 'top' ? GALAXIA_DATA.fecha_top : GALAXIA_DATA.fecha_tre);
}
function nodeWorld(i, t) {
  const p = state.pos[i];
  const v = new THREE.Vector3(p.x, p.y + Math.sin(t * 0.5 + state.phase[i]) * 1.1, p.z);
  return galaxy.localToWorld(v);
}
function refreshHi() {
  if (!hiLines) return;
  if (state.selected < 0 || !state.vis[state.selected]) { hiLines.visible = false; return; }
  const attr = hiLines.geometry.getAttribute('position');
  let k = 0, shown = 0;
  for (const [a, b] of state.edges) {
    if (a !== state.selected && b !== state.selected) continue;
    if (!state.vis[a] || !state.vis[b]) continue;
    if (shown >= 12) break;
    const A = state.pos[a], B = state.pos[b];
    attr.array[k++] = A.x; attr.array[k++] = A.y; attr.array[k++] = A.z;
    attr.array[k++] = B.x; attr.array[k++] = B.y; attr.array[k++] = B.z;
    shown++;
  }
  hiLines.geometry.setDrawRange(0, k / 3);
  attr.needsUpdate = true;
  hiLines.visible = shown > 0;
}
function select(i, fly) {
  if (i >= state.repos.length) i = -1;
  state.selected = i;
  const card = $('card');
  if (i < 0) { card.classList.remove('show'); selRing.visible = false; refreshHi(); return; }
  const r = state.repos[i];
  $('cRank').textContent = '#' + r[F.RANK];
  $('cName').textContent = r[F.FULL];
  $('cStars').innerHTML = '★ ' + fmt(r[F.STARS]);
  $('cForks').innerHTML = '⑂ ' + fmt(r[F.FORKS]);
  $('cLang').innerHTML = '<span class="langdot" style="background:' + langColor(langNorm(r[F.LANG])) + '"></span>' + (r[F.LANG] || 'Otro');
  $('cCat').textContent = r[F.CAT];
  $('cDesc').textContent = r[F.DESC] || 'Sin descripción.';
  $('cUrl').href = r[F.URL];
  card.classList.add('show');
  selRing.visible = true;
  refreshHi();
  if (fly) {
    const p = state.pos[i];
    galaxy.updateMatrixWorld();
    const dest = new THREE.Vector3(p.x, p.y, p.z).applyMatrix4(galaxy.matrixWorld);
    const dir = camera.position.clone().sub(controls.target);
    const cur = dir.length() || 1;
    dir.multiplyScalar(1 / cur);
    const want = Math.max(85, state.size[i] * 22);
    const toC = cur > want ? dest.clone().add(dir.multiplyScalar(want)) : null;
    state.tween = { from: controls.target.clone(), to: dest, fromC: camera.position.clone(), toC: toC, t: 0 };
  }
}
$('cSim').onclick = () => {
  const i = state.selected; if (i < 0) return;
  for (const [a, b] of state.edges) {
    const o = a === i ? b : b === i ? a : -1;
    if (o >= 0 && state.vis[o]) { select(o, true); return; }
  }
};
function setHoverTag(id) {
  if (id === hoverTagId) return;
  hoverTagId = id;
  if (!hoverTag) return;
  const m = hoverTag.material;
  if (m.map) { m.map.dispose(); m.map = null; }
  if (id < 0 || !state.vis[id]) { hoverTag.visible = false; return; }
  const r = state.repos[id];
  const label = '#' + r[F.RANK] + ' ' + r[F.NAME];
  const cv = document.createElement('canvas');
  let cx = cv.getContext('2d');
  cx.font = '700 24px Segoe UI, system-ui, sans-serif';
  cv.width = Math.ceil(cx.measureText(label).width) + 28; cv.height = 24 + 20;
  cx = cv.getContext('2d');
  cx.fillStyle = 'rgba(5,8,15,.92)';
  if (cx.roundRect) { cx.beginPath(); cx.roundRect(0, 0, cv.width, cv.height, 9); cx.fill(); }
  else cx.fillRect(0, 0, cv.width, cv.height);
  cx.font = '700 24px Segoe UI, system-ui, sans-serif';
  cx.fillStyle = '#ffd97a'; cx.textBaseline = 'middle';
  cx.fillText(label, 14, cv.height / 2 + 1);
  m.map = new THREE.CanvasTexture(cv); m.map.colorSpace = THREE.SRGBColorSpace;
  m.needsUpdate = true;
  hoverTag.scale.set(cv.width / 5, cv.height / 5, 1);
  hoverTag.visible = true;
}
const ray = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const tip = $('tip');
function pick(ev) {
  const rect = canvas.getBoundingClientRect();
  mouse.x = ((ev.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((ev.clientY - rect.top) / rect.height) * 2 + 1;
  ray.setFromCamera(mouse, camera);
  const hit = ray.intersectObject(nodeMesh);
  if (!hit.length) return -1;
  const id = hit[0].instanceId;
  return (id !== undefined && state.vis[id]) ? id : -1;
}
canvas.addEventListener('pointermove', ev => {
  const id = nodeMesh ? pick(ev) : -1;
  state.hover = id;
  setHoverTag(id);
  canvas.style.cursor = id >= 0 ? 'pointer' : 'grab';
  if (id >= 0) {
    const r = state.repos[id];
    tip.innerHTML = '<span>#' + r[F.RANK] + '</span> <b>' + r[F.FULL] + '</b><br>★ ' + fmt(r[F.STARS]) + ' · ' + (r[F.LANG] || 'Otro');
    tip.style.display = 'block';
    tip.style.left = (ev.clientX + 14) + 'px'; tip.style.top = (ev.clientY + 12) + 'px';
  } else tip.style.display = 'none';
});
let downX = 0, downY = 0;
canvas.addEventListener('pointerdown', ev => { downX = ev.clientX; downY = ev.clientY; });
canvas.addEventListener('click', ev => {
  if (Math.hypot(ev.clientX - downX, ev.clientY - downY) > 6) return;
  const id = nodeMesh ? pick(ev) : -1;
  select(id, id >= 0);
});
canvas.addEventListener('pointerleave', () => { tip.style.display = 'none'; setHoverTag(-1); });
$('q').addEventListener('change', () => {
  const q = $('q').value.trim().toLowerCase();
  if (!q) return;
  const i = state.repos.findIndex(r => r[F.FULL].toLowerCase().includes(q) || r[F.NAME].toLowerCase() === q);
  if (i >= 0 && state.vis[i]) select(i, true);
  else if (i >= 0) { alert('Ese repo está oculto por los filtros activos.'); }
  else alert('Sin resultados para "' + q + '".');
});
$('lang').onchange = applyFilters;
$('minStars').oninput = applyFilters;
$('topN').oninput = applyFilters;
$('bEdge').onclick = e => {
  state.showEdge = !state.showEdge;
  edgeLines.visible = state.showEdge;
  e.target.textContent = 'Conexiones: ' + (state.showEdge ? 'on' : 'off');
  e.target.classList.toggle('on', state.showEdge);
  refreshEdges();
};
$('bRot').onclick = e => {
  controls.autoRotate = !controls.autoRotate;
  e.target.textContent = 'Rotacion: ' + (controls.autoRotate ? 'on' : 'off');
  e.target.classList.toggle('on', controls.autoRotate);
};
$('bLab').onclick = e => {
  state.labels = !state.labels;
  labelGroup.visible = state.labels;
  e.target.textContent = 'Etiquetas: ' + (state.labels ? 'on' : 'off');
  e.target.classList.toggle('on', state.labels);
};
$('bReset').onclick = () => {
  camera.position.copy(CAM0); controls.target.set(0, 0, 0); select(-1);
};
function dolly(f) {
  const off = camera.position.clone().sub(controls.target);
  const len = THREE.MathUtils.clamp(off.length() * f, controls.minDistance, controls.maxDistance);
  off.setLength(len);
  camera.position.copy(controls.target).add(off);
}
$('zin').onclick = () => dolly(0.75);
$('zout').onclick = () => dolly(1.33);
$('zhome').onclick = () => { camera.position.copy(CAM0); controls.target.set(0, 0, 0); select(-1); };
$('znorth').onclick = () => {
  const off = camera.position.clone().sub(controls.target);
  const sph = new THREE.Spherical().setFromVector3(off);
  sph.theta = 0;
  off.setFromSpherical(sph);
  camera.position.copy(controls.target).add(off);
};
$('zfull').onclick = e => {
  if (!document.fullscreenElement) document.documentElement.requestFullscreen().catch(() => {});
  else document.exitFullscreen();
};
function toggleUI(force) {
  const hide = force !== undefined ? force : !document.body.classList.contains('uihidden');
  document.body.classList.toggle('uihidden', hide);
  $('zui').classList.toggle('on', !hide);
}
$('zui').onclick = () => toggleUI();
document.querySelectorAll('.minbtn[data-min]').forEach(b => {
  b.onclick = () => {
    const el = $(b.dataset.min);
    el.classList.toggle('min');
    b.textContent = el.classList.contains('min') ? '+' : '—';
  };
});
$('cardX').onclick = () => select(-1);
canvas.addEventListener('dblclick', ev => {
  const id = nodeMesh ? pick(ev) : -1;
  if (id >= 0) select(id, true);
});
window.addEventListener('keydown', ev => {
  if (ev.target && (ev.target.tagName === 'INPUT' || ev.target.tagName === 'SELECT')) return;
  const k = ev.key.toLowerCase();
  if (k === '+' || k === '=') dolly(0.8);
  else if (k === '-') dolly(1.25);
  else if (k === '0') $('zhome').click();
  else if (k === 'n') $('znorth').click();
  else if (k === 'f') $('zfull').click();
  else if (k === 'h') toggleUI();
  else if (k === 'escape') select(-1);
});
$('mTop').onclick = () => { if (state.mode !== 'top') { state.mode = 'top'; $('mTop').classList.add('on'); $('mTre').classList.remove('on'); $('minStars').value = 0; select(-1); buildGalaxy(); } };
$('mTre').onclick = () => { if (state.mode !== 'tre') { state.mode = 'tre'; $('mTre').classList.add('on'); $('mTop').classList.remove('on'); $('minStars').value = 0; select(-1); buildGalaxy(); } };
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
let lastT = performance.now(), frames = 0, fpsT = 0;
function animate(now) {
  requestAnimationFrame(animate);
  const t = now / 1000;
  if (state.tween) {
    const tw = state.tween;
    tw.t = Math.min(1, tw.t + 0.03);
    const k = tw.t * tw.t * (3 - 2 * tw.t);
    controls.target.lerpVectors(tw.from, tw.to, k);
    if (tw.toC) camera.position.lerpVectors(tw.fromC, tw.toC, k);
    if (tw.t >= 1) state.tween = null;
  }
  if (nodeMesh) {
    for (let i = 0; i < state.repos.length; i++) {
      const p = state.pos[i];
      const bob = Math.sin(t * 0.5 + state.phase[i]) * 1.1;
      const s = state.vis[i] ? state.size[i] : 0.0001;
      dummy.position.set(p.x, p.y + bob, p.z);
      dummy.scale.setScalar(s); dummy.updateMatrix();
      nodeMesh.setMatrixAt(i, dummy.matrix);
      dummy.scale.setScalar(s * 1.9); dummy.updateMatrix();
      glowMesh.setMatrixAt(i, dummy.matrix);
    }
    nodeMesh.instanceMatrix.needsUpdate = true;
    glowMesh.instanceMatrix.needsUpdate = true;
  }
  if (selRing && selRing.visible && state.selected >= 0) {
    const w = nodeWorld(state.selected, t);
    selRing.position.copy(w);
    selRing.lookAt(camera.position);
    const s = state.size[state.selected] * (1.7 + 0.15 * Math.sin(t * 3));
    selRing.scale.setScalar(Math.max(0.1, s));
  }
  if (hoverTag) {
    if (hoverTagId >= 0 && state.vis[hoverTagId]) {
      const p = state.pos[hoverTagId];
      hoverTag.position.set(p.x, p.y + Math.sin(t * 0.5 + state.phase[hoverTagId]) * 1.1 + state.size[hoverTagId] + 8, p.z);
      hoverTag.visible = true;
    } else hoverTag.visible = false;
  }
  stars.rotation.y = (stars.rotation.y + 0.00004) % (Math.PI * 2);
  controls.update();
  renderer.render(scene, camera);
  frames++; fpsT += now - lastT; lastT = now;
  if (fpsT >= 1000) {
    $('stFps').textContent = Math.round(frames * 1000 / fpsT); frames = 0; fpsT = 0;
    const _off = camera.position.clone().sub(controls.target);
    const _th = new THREE.Spherical().setFromVector3(_off).theta;
    $('needle').style.transform = 'rotate(' + (-_th * 180 / Math.PI) + 'deg)';
  }
}
buildGalaxy();
requestAnimationFrame(animate);
</script>
</body></html>"""

html = TEMPLATE.replace("__UMAMI__", UMAMI).replace("__GALAXIA_JSON__", DATA_JS)
assert "codecrafters-io/build-your-own-x" in html, "falta marcador top500"
assert "lnkiai/m3e-canvas" in html, "falta marcador trending"
out = os.path.join(SITE, "galaxia.html")
open(out, "w", encoding="utf-8").write(html)
print("galaxia.html OK: %d KB (top=%d, tre=%d)" % (len(html) // 1024, len(payload["top"]), len(payload["tre"])))
