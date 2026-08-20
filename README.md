# Web Data Extractor

> Automatización y extracción de información web utilizando Python, Playwright y Selenium.

## Descripción

**Web Data Extractor** es un proyecto de automatización web desarrollado en Python que permite navegar por páginas web, extraer información relevante y almacenar los resultados en diferentes formatos.

El proyecto fue creado como práctica y demostración de conocimientos en **Web Automation, Web Scraping y Testing Automation**, utilizando herramientas como **Playwright** y **Selenium**.

Actualmente, el script puede recorrer páginas web, analizar su contenido y extraer información como títulos, nombres, precios, enlaces y contenido visible.

## Tecnologías utilizadas

- Python
- Playwright
- Selenium
- Web Automation
- Web Scraping
- CSV
- JSON
- Regular Expressions

## Funcionalidades

- Navegación automatizada.
- Extracción de títulos y nombres.
- Detección de precios mediante expresiones regulares.
- Extracción de enlaces internos.
- Recorrido automático de múltiples páginas.
- Control de URLs visitadas.
- Manejo básico de errores.
- Espera de contenido dinámico.
- Exportación de información a CSV.
- Exportación de información a JSON.
- Automatización compatible con páginas modernas que utilizan JavaScript.

## Estructura del proyecto

```text
web-data-extractor/
│
├── extraer_demoqa.py
├── demoqa_datos.csv
├── demoqa_datos.json
├── requirements.txt
└── README.md
```

## Instalación

Clona el repositorio:

```bash
git clone https://github.com/TU-USUARIO/TU-REPOSITORIO.git
```

Accede a la carpeta:

```bash
cd TU-REPOSITORIO
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

Instala los navegadores necesarios para Playwright:

```bash
playwright install
```

## Ejecución

Ejecuta el script principal:

```bash
python extraer_demoqa.py
```

El navegador se abrirá automáticamente y comenzará el proceso de navegación y extracción.

## Resultados

Una vez finalizado el proceso, se generarán archivos con la información extraída:

```text
demoqa_datos.csv
demoqa_datos.json
```

Ejemplo de información almacenada:

| Nombre | Precio | URL |
|---|---|---|
| Elements | No encontrado | https://demoqa.com/elements |
| Forms | No encontrado | https://demoqa.com/forms |
| Alerts | No encontrado | https://demoqa.com/alertsWindows |
| Widgets | No encontrado | https://demoqa.com/widgets |

> DemoQA es una plataforma de práctica para automatización web, por lo que no contiene productos comerciales ni precios reales.

## Playwright

El proyecto utiliza **Playwright** para controlar el navegador y automatizar acciones como:

```python
page.goto(url)
page.locator("body").inner_text()
page.locator("a")
page.wait_for_timeout(1500)
```

Playwright permite trabajar con aplicaciones web modernas y contenido generado dinámicamente con JavaScript.

## Selenium

El proyecto también puede extenderse utilizando **Selenium WebDriver**, una de las herramientas más utilizadas en automatización y pruebas web.

Ejemplo básico:

```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://demoqa.com")

titulo = driver.title
print(titulo)

driver.quit()
```

## Próximas mejoras

- Exportación directa a Excel `.xlsx`.
- Integración con bases de datos.
- Soporte para múltiples sitios web.
- Sistema de configuración mediante `.env`.
- Ejecución en modo headless.
- Scroll automático.
- Manejo de paginación.
- Extracción automática de imágenes.
- Detección avanzada de productos.
- Implementación de Selenium y Playwright como módulos independientes.
- Dashboard para visualizar los datos extraídos.

## Objetivo del proyecto

Este proyecto forma parte de mi portafolio y tiene como objetivo demostrar conocimientos prácticos en:

```text
Python
│
├── Automatización Web
├── Web Scraping
├── Playwright
├── Selenium
├── Manejo del DOM
├── Expresiones Regulares
├── Manejo de Archivos
├── CSV / JSON
└── Automatización de Navegadores
```

## Autor

**Javier Castellanos**

Estudiante de Ingeniería en Sistemas e interesado en automatización de procesos, desarrollo de software, bots y tecnologías web.

### Tecnologías principales

`Python` · `Playwright` · `Selenium` · `JavaScript` · `HTML` · `CSS` · `Git` · `GitHub`

---

⭐ Si este proyecto te resulta interesante, puedes dejar una estrella en el repositorio.
