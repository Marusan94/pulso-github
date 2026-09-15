import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data")

PROPOSITO = {
    "IA/LLM": "crear aplicaciones con modelos de lenguaje, agentes inteligentes y automatizacion",
    "Frontend": "construir interfaces web modernas, rapidas y reactivas",
    "Educación/Recursos": "aprender programacion y descubrir recursos seleccionados",
    "Backend/DevOps": "montar servidores, API e infraestructura lista para produccion",
    "Templates": "arrancar proyectos nuevos con plantillas ya armadas",
    "Seguridad": "auditar, proteger y entender la seguridad de los sistemas",
    "DevTools": "agilizar el trabajo diario de desarrollo de software",
}
TIPO_FRASE = {
    "awesome-list": "Es una lista curada de recursos",
    "educativo": "Es material educativo para estudiar",
    "framework/librería": "Es un framework o libreria",
    "herramienta/app": "Es una herramienta o aplicacion",
}

def miles(n):
    if n >= 1000:
        v = n / 1000
        return ("%g" % round(v, 1)) + " mil"
    return str(n)

def build_es(x):
    lang = x.get("language") or "varios lenguajes"
    if lang == "—":
        lang = "varios lenguajes"
    base = "%s de %s en %s para %s." % (
        TIPO_FRASE.get(x.get("tipo"), "Es un proyecto"),
        (x.get("categoria") or "software").lower(),
        lang,
        PROPOSITO.get(x.get("categoria"), "usar en tus proyectos"),
    )
    comunidad = "Suma %s estrellas y %s bifurcaciones" % (miles(x.get("stars", 0)), miles(x.get("forks", 0)))
    fecha = x.get("created_at") or x.get("pushed_at")
    if fecha:
        comunidad += ", con actividad registrada el %s" % fecha
    comunidad += "."
    extra = ""
    if x.get("archived"):
        extra = " Esta archivado: sirve como referencia, ya no acepta cambios."
    lic = (x.get("license") or "—")
    if lic not in ("—", "NOASSERTION", ""):
        extra += " Licencia %s." % lic
    return base + " " + comunidad + extra

for fn in ("repos.json", "trending.json"):
    p = os.path.join(SRC, fn)
    d = json.load(open(p, encoding="utf-8"))
    for x in d["repos"]:
        x["descripcion_es"] = build_es(x)
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False)
    print(fn, len(d["repos"]), "con descripcion_es")
    print("EJ:", d["repos"][0]["full_name"], "->", d["repos"][0]["descripcion_es"][:160])
