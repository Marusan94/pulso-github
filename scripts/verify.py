"""Valida el sitio: JS sintacticamente correcto (node --check),
ambas bases embebidas y conteos esperados."""
import glob, json, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "docs")
DATA = os.path.join(ROOT, "data")

top = json.load(open(os.path.join(DATA, "repos.json"), encoding="utf-8"))["repos"]
tre = json.load(open(os.path.join(DATA, "trending.json"), encoding="utf-8"))["repos"]
assert len(top) == 500, f"repos.json trae {len(top)}, espero 500"
assert len(tre) >= 100, f"trending.json trae {len(tre)}, espero >=100"
assert all(x.get("descripcion_es") for x in top + tre), "falta descripcion_es"
print(f"datos OK: {len(top)} top + {len(tre)} trending, todos con descripcion_es")

fails = 0
SIN_DB = {"index.html", "404.html", "como-esta-hecho.html"}  # sin base embebida por diseño
for f in sorted(glob.glob(os.path.join(SITE, "*.html"))):
    t = open(f, encoding="utf-8").read()
    name = os.path.basename(f)
    inline = re.findall(r"<script>(.*?)</script>", t, re.S)
    if not inline:
        if name in SIN_DB:
            print(name, "OK (sin JS por diseño)")
            continue
        print(name, "SIN script inline"); fails += 1; continue
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tmp:
        tmp.write(inline[0])
        tp = tmp.name
    r = subprocess.run(["node", "--check", tp], capture_output=True, text=True)
    os.unlink(tp)
    if name in SIN_DB:
        status = "OK" if r.returncode == 0 else "FALLO"
    else:
        ok_db = "codecrafters-io/build-your-own-x" in t and "lnkiai/m3e-canvas" in t
        status = "OK" if r.returncode == 0 and ok_db else "FALLO"
    if status == "FALLO":
        fails += 1
    print(name, status)
con_track = []
for f in sorted(glob.glob(os.path.join(SITE, "*.html"))):
    t = open(f, encoding="utf-8").read()
    if "data-website-id" not in t:
        continue
    con_track.append(os.path.basename(f))
    src = re.search(r'<script[^>]*src="(https://[^"]+)"[^>]*data-website-id="([^"]+)"', t)
    src = src or re.search(r'<script[^>]*data-website-id="([^"]+)"[^>]*src="(https://[^"]+)"', t)
    if not src or not src.group(1) or not src.group(2):
        print(os.path.basename(f), "UMAMI MALFORMADO")
        fails += 1
if con_track and not fails:
    print(f"umami OK: tracker de producción en {len(con_track)} páginas")
else:
    print("umami OK (build local, sin tracker)")
def _lum(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def _ratio(a, b):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)
for f in sorted(glob.glob(os.path.join(SITE, "*.html"))):
    t = open(f, encoding="utf-8").read()
    m = re.search(r":root\{([^}]*)\}", t)
    if not m or "--ink" not in m.group(1):
        continue
    v = dict(re.findall(r"(--\w+):([^;]+);", m.group(1)))
    try:
        ib, mb, aa = _ratio(v["--ink"], v["--bg"]), _ratio(v["--mut"], v["--bg"]), _ratio(v["--acc"], v["--acctext"])
    except (KeyError, ValueError):
        print(os.path.basename(f), "CONTRASTE SIN MEDIR"); fails += 1; continue
    estado = "OK" if (ib >= 7 and mb >= 3 and aa >= 3) else "FALLO"
    aviso = "" if aa >= 4.5 else " (AVISO: botones bajo 4.5)"
    print(os.path.basename(f), f"contraste {estado} ink/bg={ib:.1f} mut/bg={mb:.1f} acc/txt={aa:.1f}" + aviso)
    if estado == "FALLO":
        fails += 1
print("FALLOS:", fails)
sys.exit(1 if fails else 0)
