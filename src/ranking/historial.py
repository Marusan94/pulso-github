"""Historial compartido: deltas y series contra data/history/.

Unifica las variantes duplicadas en build_site.py y build_paginas.py.
`deltas` devuelve el superconjunto (diffs, fecha_previa, ranking_previo);
quien no necesite el ranking previo lo ignora.
"""
import glob
import os


def _snaps(data_dir, kind):
    return sorted(glob.glob(os.path.join(data_dir, "history", "*-" + kind + ".json")))


def deltas(kind, current, data_dir):
    """Diferencia de estrellas y puesto previo vs el snapshot anterior.

    Devuelve (diffs, fecha_previa, ranking_previo).
    """
    import json
    snaps = _snaps(data_dir, kind)
    prevs = [s for s in snaps if os.path.basename(s)[:10] < current.get("fecha", "")]
    if not prevs:
        return {}, "", {}
    prev = json.load(open(prevs[-1], encoding="utf-8"))
    old = {r["n"]: r["s"] for r in prev["repos"]}
    prank = {r["n"]: i + 1 for i, r in enumerate(sorted(prev["repos"], key=lambda r: -r["s"]))}
    diffs = {x["full_name"]: x["stars"] - old.get(x["full_name"], x["stars"])
             for x in current["repos"]}
    return diffs, prev["fecha"], prank


def series(kind, current, data_dir):
    """Puntos [fecha, estrellas] por repo, incluyendo el corte actual."""
    import json
    por_repo = {}
    for s in _snaps(data_dir, kind):
        d = json.load(open(s, encoding="utf-8"))
        for r in d["repos"]:
            por_repo.setdefault(r["n"], []).append([d["fecha"], r["s"]])
    for x in current["repos"]:
        lst = por_repo.setdefault(x["full_name"], [])
        if not lst or lst[-1][0] != current.get("fecha", ""):
            lst.append([current.get("fecha", ""), x["stars"]])
    return por_repo
