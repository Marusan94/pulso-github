import urllib.request, json, time, os
import datetime
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.ranking.taxonomia import categoria, tipo
out_dir = os.path.join(ROOT, "data")
os.makedirs(out_dir, exist_ok=True)
HOY = datetime.date.today().isoformat()
TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {"User-Agent": "opencode", "Accept": "application/vnd.github+json"}
if TOKEN:
    HEADERS["Authorization"] = "Bearer " + TOKEN
all_items = []
for page in range(1, 6):
    url = f"https://api.github.com/search/repositories?q=stars:%3E20000&sort=stars&order=desc&per_page=100&page={page}"
    req = urllib.request.Request(url, headers=HEADERS)
    print("fetch page",page,flush=True)
    with urllib.request.urlopen(req, timeout=30) as r:
        data=json.load(r)
        items=data.get("items",[])
        print(f"page {page}: {len(items)} items",flush=True)
        all_items.extend(items)
    if page<5:
        time.sleep(8)
print("total",len(all_items))

repos=[]
for i,it in enumerate(all_items[:500], start=1):
    repos.append({
        "rank": i,
        "full_name": it.get("full_name"),
        "name": it.get("name"),
        "description": it.get("description") or "",
        "stars": it.get("stargazers_count"),
        "forks": it.get("forks_count"),
        "language": it.get("language") or "—",
        "license": (it.get("license") or {}).get("spdx_id") or "—",
        "pushed_at": (it.get("pushed_at") or "")[:10],
        "archived": it.get("archived"),
        "url": it.get("html_url"),
        "categoria": categoria(it.get("full_name"), it.get("description")),
        "tipo": tipo(it.get("full_name"), it.get("description")),
    })
with open(os.path.join(out_dir,"repos.json"),"w",encoding="utf-8") as f:
    json.dump({"fecha": HOY,"total":len(repos),"repos":repos}, f, ensure_ascii=False)
print("saved", len(repos))
