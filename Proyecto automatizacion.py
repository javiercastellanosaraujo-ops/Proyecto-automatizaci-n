from playwright.sync_api import sync_playwright
import csv
import json
import re
from urllib.parse import urljoin, urlparse


BASE_URL = "https://demoqa.com"
MAX_PAGES = 50


def limpiar_texto(texto):
    if not texto:
        return ""

    return " ".join(texto.split())


def buscar_precio(texto):
    """
    Busca posibles precios dentro de un texto.
    Ejemplos:
    $10.99
    €20
    15.000 USD
    """
    patrones = [
        r"\$\s?\d+(?:[.,]\d{1,2})?",
        r"€\s?\d+(?:[.,]\d{1,2})?",
        r"£\s?\d+(?:[.,]\d{1,2})?",
        r"\d+(?:[.,]\d{1,2})?\s?(?:USD|EUR|USDT|Bs|VES)"
    ]

    for patron in patrones:
        resultado = re.search(patron, texto, re.IGNORECASE)

        if resultado:
            return resultado.group()

    return ""


def es_url_valida(url):
    try:
        dominio = urlparse(url).netloc
        return dominio == "demoqa.com"
    except Exception:
        return False


def main():

    datos_extraidos = []
    urls_visitadas = set()
    urls_pendientes = [BASE_URL]

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page(
            viewport={
                "width": 1440,
                "height": 900
            }
        )

        while urls_pendientes and len(urls_visitadas) < MAX_PAGES:

            url = urls_pendientes.pop(0)

            if url in urls_visitadas:
                continue

            try:
                print(f"\nVisitando: {url}")

                page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=30000
                )

                page.wait_for_timeout(1500)

                urls_visitadas.add(url)

                titulo = limpiar_texto(
                    page.title()
                )

                contenido = limpiar_texto(
                    page.locator("body").inner_text()
                )

                precio = buscar_precio(contenido)

                # Intentamos encontrar un nombre o título principal
                nombre = ""

                for selector in ["h1", "h2", ".main-header"]:

                    elementos = page.locator(selector)

                    if elementos.count() > 0:

                        nombre = limpiar_texto(
                            elementos.first.inner_text()
                        )

                        if nombre:
                            break

                if not nombre:
                    nombre = titulo

                datos = {
                    "nombre": nombre,
                    "precio": precio if precio else "No encontrado",
                    "titulo_pagina": titulo,
                    "url": url,
                    "contenido": contenido[:5000]
                }

                datos_extraidos.append(datos)

                print(f"Nombre: {nombre}")
                print(f"Precio: {precio if precio else 'No encontrado'}")

                # Extraer enlaces de la página
                enlaces = page.locator("a")

                cantidad = enlaces.count()

                for i in range(cantidad):

                    try:

                        href = enlaces.nth(i).get_attribute("href")

                        if not href:
                            continue

                        url_completa = urljoin(url, href)

                        # Quitamos fragmentos tipo #algo
                        url_completa = url_completa.split("#")[0]

                        if (
                            url_completa
                            and es_url_valida(url_completa)
                            and url_completa not in urls_visitadas
                            and url_completa not in urls_pendientes
                        ):

                            urls_pendientes.append(
                                url_completa
                            )

                    except Exception:
                        pass

            except Exception as e:

                print(
                    f"Error procesando {url}: {e}"
                )

        browser.close()

    # -------------------------
    # GUARDAR EN JSON
    # -------------------------

    with open(
        "demoqa_datos.json",
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos_extraidos,
            archivo,
            ensure_ascii=False,
            indent=4
        )

    # -------------------------
    # GUARDAR EN CSV
    # -------------------------

    with open(
        "demoqa_datos.csv",
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as archivo:

        campos = [
            "nombre",
            "precio",
            "titulo_pagina",
            "url",
            "contenido"
        ]

        writer = csv.DictWriter(
            archivo,
            fieldnames=campos
        )

        writer.writeheader()

        writer.writerows(
            datos_extraidos
        )

    print("\n==============================")
    print("EXTRACCIÓN FINALIZADA")
    print("==============================")

    print(
        f"Páginas procesadas: {len(datos_extraidos)}"
    )

    print(
        "Archivos generados:"
    )

    print("- demoqa_datos.json")
    print("- demoqa_datos.csv")


if __name__ == "__main__":
    main()