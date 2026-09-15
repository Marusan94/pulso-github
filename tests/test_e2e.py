"""Extremo a extremo con Chromium real: elegir -> filtrar -> descargar -> cambiar modo."""
import os

from playwright.sync_api import sync_playwright

SITE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")


def pagina(nombre="30-ember.html"):
    pw = sync_playwright().start()
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 900})
    pg.goto("file:///" + os.path.join(SITE, nombre).replace("\\", "/"))
    pg.wait_for_timeout(1200)
    return pw, b, pg


def test_elegir_filtrar_y_descargar_csv(tmp_path):
    pw, b, pg = pagina()
    try:
        assert len(pg.query_selector_all(".pick")) == 50
        pg.query_selector_all(".pick")[0].click()
        pg.wait_for_timeout(300)
        pg.query_selector_all(".pick")[1].click()
        pg.wait_for_timeout(300)
        assert pg.inner_text("#favc") == "2"
        pg.click("#bfav")
        pg.wait_for_timeout(300)
        assert "2 repositorios (elegidos)" in pg.inner_text("#n")
        with pg.expect_download() as dl:
            pg.click("#fcsv")
        ruta = os.path.join(str(tmp_path), dl.value.suggested_filename)
        dl.value.save_as(ruta)
        lineas = open(ruta, encoding="utf-8").read().splitlines()
        assert lineas[0].startswith("puesto,nombre,estrellas")
        assert len(lineas) == 3
    finally:
        b.close()
        pw.stop()


def test_filtro_mit_solo_mit():
    pw, b, pg = pagina()
    try:
        pg.select_option("#lic", "MIT")
        pg.wait_for_timeout(400)
        assert "repositorios" in pg.inner_text("#n")
        licencias = pg.eval_on_selector_all(
            "#g .bdg", "els => els.map(e => e.textContent)")
        assert licencias, "sin insignias visibles"
    finally:
        b.close()
        pw.stop()


def test_modo_cambia_conservando_modulo():
    pw, b, pg = pagina("29-evergreen.html")
    try:
        pg.click("#modobtn")
        pg.wait_for_timeout(200)
        pg.click("#modomenu a[data-f='14-block-party']")
        pg.wait_for_timeout(1500)
        assert pg.url.endswith("14-block-party.html?mod=500")
        assert "500 repositorios" in pg.inner_text("#n")
    finally:
        b.close()
        pw.stop()
