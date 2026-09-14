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
SIN_DB = {"index.html", "404.html"}  # landing y error: sin base embebida por diseño
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
print("FALLOS:", fails)
sys.exit(1 if fails else 0)
