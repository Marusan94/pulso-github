import urllib.request, json, time, os
import datetime
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.ranking.taxonomia import categoria, tipo
out_dir = os.path.join(ROOT, "data")
HOY = datetime.date.today().isoformat()
DESDE = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {"User-Agent": "opencode", "Accept": "application/vnd.github+json"}
if TOKEN:
    HEADERS["Authorization"] = "Bearer " + TOKEN

all_items = []
for page in range(1, 3):
    url = "https://api.github.com/search/repositories?q=created:%3E" + DESDE + "&sort=stars&order=desc&per_page=100&page=" + str(page)
    req = urllib.request.Request(url, headers=HEADERS)
    print("fetch trending page", page, flush=True)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
        items = data.get("items", [])
        print(f"page {page}: {len(items)} items", flush=True)
        all_items.extend(items)
    if page < 2:
        time.sleep(8)

repos = []
for i, it in enumerate(all_items, start=1):
    repos.append({
        "rank": i,
        "full_name": it.get("full_name"),
        "description": it.get("description") or "",
        "stars": it.get("stargazers_count"),
        "forks": it.get("forks_count"),
        "language": it.get("language") or "—",
        "license": (it.get("license") or {}).get("spdx_id") or "—",
        "created_at": (it.get("created_at") or "")[:10],
        "pushed_at": (it.get("pushed_at") or "")[:10],
        "archived": it.get("archived"),
        "url": it.get("html_url"),
        "categoria": categoria(it.get("full_name"), it.get("description")),
        "tipo": tipo(it.get("full_name"), it.get("description")),
    })
with open(os.path.join(out_dir, "trending.json"), "w", encoding="utf-8") as f:
    json.dump({"fecha": HOY, "ventana": "creados desde " + DESDE, "total": len(repos), "repos": repos}, f, ensure_ascii=False)
print("saved trending:", len(repos))
for x in repos[:8]:
    print(x["created_at"], x["stars"], x["full_name"])
