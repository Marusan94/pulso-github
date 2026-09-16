"""Fechas derivadas de los datos (nada hardcodeado en los builds)."""
import datetime

MESES = ["ene", "feb", "mar", "abr", "may", "jun",
         "jul", "ago", "sep", "oct", "nov", "dic"]


def hoy_iso():
    return datetime.date.today().isoformat()


def fecha_corta(iso):
    """'2026-09-15' -> '15 sep 2026'."""
    try:
        y, m, d = iso.split("-")
        return f"{int(d)} {MESES[int(m) - 1]} {y}"
    except (ValueError, AttributeError, IndexError):
        return iso or ""


def dias_atras(iso, n):
    """Resta n días a una fecha ISO."""
    try:
        y, m, d = (int(v) for v in iso.split("-"))
        return (datetime.date(y, m, d) - datetime.timedelta(days=n)).isoformat()
    except (ValueError, AttributeError):
        return iso or ""
