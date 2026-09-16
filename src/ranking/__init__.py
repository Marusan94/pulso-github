"""Lógica compartida del ranking: taxonomía, historial y fechas.

Única fuente de verdad para categorizar repos y para calcular
deltas/series contra data/history/. Los scripts de fetch y build
importan de aquí en vez de duplicar el código.
"""
from .taxonomia import categoria, tipo, PERMISIVAS
from .historial import deltas, series
from .fechas import fecha_corta, hoy_iso

__all__ = ["categoria", "tipo", "PERMISIVAS", "deltas", "series", "fecha_corta", "hoy_iso"]
