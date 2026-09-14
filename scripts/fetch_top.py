import urllib.request, json, time, os
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out_dir = os.path.join(ROOT, "data")
os.makedirs(out_dir, exist_ok=True)
all_items=[]
for page in range(1,6):
    url=f"https://api.github.com/search/repositories?q=stars:%3E20000&sort=stars&order=desc&per_page=100&page={page}"
    req=urllib.request.Request(url, headers={"User-Agent":"opencode","Accept":"application/vnd.github+json"})
    print("fetch page",page,flush=True)
    with urllib.request.urlopen(req, timeout=30) as r:
        data=json.load(r)
        items=data.get("items",[])
        print(f"page {page}: {len(items)} items",flush=True)
        all_items.extend(items)
    if page<5:
        time.sleep(8)
print("total",len(all_items))

def categoria(name, desc):
    t=((name or "")+" "+(desc or "")).lower()
    if any(k in t for k in ["llm","gpt","agent","ai ","artificial","diffusion","stable","langchain","openclaw","hermes","mcp","skill","transformer","chatbot"]): return "IA/LLM"
    if any(k in t for k in ["react","vue","angular","frontend","css","tailwind","ui ","component"]): return "Frontend"
    if any(k in t for k in ["awesome","list of","curated","roadmap","interview","tutorial","book","course","learn","primer","university"]): return "Educación/Recursos"
    if any(k in t for k in ["api","framework","server","database","kubernetes","docker","cli ","terminal","linux","kernel","self-host"]): return "Backend/DevOps"
    if any(k in t for k in ["admin","dashboard","template","boilerplate"]): return "Templates"
    if any(k in t for k in ["security","hack","cheat","exploit"]): return "Seguridad"
    return "DevTools"

def tipo(name, desc):
    t=((name or "")+" "+(desc or "")).lower()
    if "awesome" in t or "list of" in t or "curated list" in t: return "awesome-list"
    if any(k in t for k in ["tutorial","course","book","roadmap","university","primer","learn"]): return "educativo"
    if any(k in t for k in ["framework","library","kernel"]): return "framework/librería"
    return "herramienta/app"

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
    json.dump({"fecha":"2026-09-14","total":len(repos),"repos":repos}, f, ensure_ascii=False)
print("saved", len(repos))
