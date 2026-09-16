import os
SITE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
BASE = (os.environ.get("SITE_URL") or "https://TU-DOMINIO").rstrip("/")
pages = [""] + [f[:-5] for f in sorted(os.listdir(SITE)) if f.endswith(".html") and f not in ("index.html", "404.html")]
xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for pg in pages:
    xml.append(f"  <url><loc>{BASE}/{pg}</loc><changefreq>weekly</changefreq></url>")
xml.append("</urlset>")
open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(xml))
print("sitemap ok:", len(pages), "urls (cambia TU-DOMINIO por tu dominio real)")
