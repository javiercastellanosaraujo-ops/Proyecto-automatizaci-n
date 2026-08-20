import csv
import json
import re
import time
from urllib.parse import urljoin, urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException
)


BASE_URL = "https://demoqa.com"
MAX_PAGES = 50


def limpiar_texto(texto):
    """Limpia espacios y saltos de línea innecesarios."""
    if not texto:
        return ""

    return " ".join(texto.split())


def buscar_precio(texto):
    """Busca posibles precios dentro del texto."""

    patrones = [
        r"\$\s?\d+(?:[.,]\d{1,2})?",
        r"€\s?\d+(?:[.,]\d{1,2})?",
        r"£\s?\d+(?:[.,]\d{1,2})?",
        r"\d+(?:[.,]\d{1,2})?\s?(?:USD|EUR|USDT|Bs|VES)"
    ]

    for patron in patrones:
        resultado = re.search(
            patron,
            texto,
            re.IGNORECASE
        )

        if resultado:
            return resultado.group()

    return ""


def es_url_valida(url):
    """Comprueba que la URL pertenezca a demoqa.com."""

    try:
        dominio = urlparse(url).netloc

        return dominio == "demoqa.com"

    except Exception:
        return False


def obtener_nombre(driver):
    """Intenta obtener el título principal de la página."""

    selectores = [
        "h1",
        ".main-header",
        "h2"
    ]

    for selector in selectores:

        try:
            elementos = driver.find_elements(
                By.CSS_SELECTOR,
                selector
            )

            if elementos:

                nombre = limpiar_texto(
                    elementos[0].text
                )

                if nombre:
                    return nombre

        except Exception:
            pass

    return limpiar_texto(driver.title)


def configurar_navegador():

    opciones = Options()

    # Si quieres ejecutar el navegador oculto,
    # elimina el comentario de la siguiente línea:
    # opciones.add_argument("--headless=new")

    opciones.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        options=opciones
    )

    driver.set_page_load_timeout(30)

    return driver


def main():

    datos_extraidos = []

    urls_visitadas = set()

    urls_pendientes = [
        BASE_URL
    ]

    driver = configurar_navegador()

    try:

        while (
            urls_pendientes
            and len(urls_visitadas) < MAX_PAGES
        ):

            url = urls_pendientes.pop(0)

            if url in urls_visitadas:
                continue

            try:

                print(f"\nVisitando: {url}")

                driver.get(url)

                # Pequeña espera para contenido dinámico
                time.sleep(1.5)

                urls_visitadas.add(url)

                titulo = limpiar_texto(
                    driver.title
                )

                contenido = limpiar_texto(
                    driver.find_element(
                        By.TAG_NAME,
                        "body"
                    ).text
                )

                nombre = obtener_nombre(
                    driver
                )

                precio = buscar_precio(
                    contenido
                )

                datos = {
                    "nombre": nombre,
                    "precio": (
                        precio
                        if precio
                        else "No encontrado"
                    ),
                    "titulo_pagina": titulo,
                    "url": url,
                    "contenido": contenido[:5000]
                }

                datos_extraidos.append(
                    datos
                )

                print(
                    f"Nombre: {nombre}"
                )

                print(
                    f"Precio: "
                    f"{precio if precio else 'No encontrado'}"
                )

                # Extraer todos los enlaces
                enlaces = driver.find_elements(
                    By.TAG_NAME,
                    "a"
                )

                for enlace in enlaces:

                    try:

                        href = enlace.get_attribute(
                            "href"
                        )

                        if not href:
                            continue

                        url_completa = urljoin(
                            url,
                            href
                        )

                        # Eliminar fragmentos como #contacto
                        url_completa = (
                            url_completa.split("#")[0]
                        )

                        if (
                            url_completa
                            and es_url_valida(
                                url_completa
                            )
                            and url_completa
                            not in urls_visitadas
                            and url_completa
                            not in urls_pendientes
                        ):

                            urls_pendientes.append(
                                url_completa
                            )

                    except Exception:
                        pass

            except TimeoutException:

                print(
                    f"Tiempo agotado: {url}"
                )

            except WebDriverException as e:

                print(
                    f"Error en {url}: {e}"
                )

            except Exception as e:

                print(
                    f"Error inesperado "
                    f"en {url}: {e}"
                )

    finally:

        driver.quit()

    # =========================
    # GUARDAR JSON
    # =========================

    with open(
        "demoqa_selenium_datos.json",
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos_extraidos,
            archivo,
            ensure_ascii=False,
            indent=4
        )

    # =========================
    # GUARDAR CSV
    # =========================

    with open(
        "demoqa_selenium_datos.csv",
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

    print("\n" + "=" * 40)
    print("EXTRACCIÓN CON SELENIUM FINALIZADA")
    print("=" * 40)

    print(
        f"Páginas procesadas: "
        f"{len(datos_extraidos)}"
    )

    print(
        "\nArchivos generados:"
    )

    print(
        "- demoqa_selenium_datos.csv"
    )

    print(
        "- demoqa_selenium_datos.json"
    )


if __name__ == "__main__":
    main()