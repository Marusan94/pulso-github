"""Archiva el corte actual en data/history/ (base del historial y la API versionada)."""
import json
import os

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
HIST = os.path.join(DATA, "history")
os.makedirs(HIST, exist_ok=True)


def snap(origen, prefijo):
    data = json.load(open(os.path.join(DATA, origen), encoding="utf-8"))
    fecha = data.get("fecha", "sin-fecha")
    destino = os.path.join(HIST, f"{fecha}-{prefijo}.json")
    if os.path.exists(destino):
        print("ya existe", os.path.basename(destino))
        return
    mini = [{"n": x["full_name"], "s": x["stars"], "f": x["forks"]} for x in data["repos"]]
    json.dump({"fecha": fecha, "total": len(mini), "repos": mini},
              open(destino, "w", encoding="utf-8"), ensure_ascii=False)
    print("snapshot", os.path.basename(destino), len(mini))


snap("repos.json", "top")
snap("trending.json", "tre")
