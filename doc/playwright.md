# Playwright: pruebas y automatización web

Playwright permite controlar navegadores mediante código. Se puede utilizar
para comprobar que una aplicación web funciona correctamente o para
automatizar tareas repetitivas realizadas en el navegador.

Con Playwright se pueden abrir páginas, pulsar botones, escribir en
formularios, descargar archivos, realizar capturas y comprobar resultados.
Funciona con navegadores basados en Chromium, Firefox y WebKit.

## Instalar Playwright

Si el proyecto utiliza `uv`, se puede instalar como dependencia de desarrollo:

```powershell
uv add --dev playwright
```

Después es necesario instalar los navegadores compatibles:

```powershell
uv run playwright install
```

La descarga requiere conexión a Internet. En Linux, algunos sistemas también
pueden necesitar dependencias del sistema operativo, que Playwright puede
ayudar a instalar con `playwright install --with-deps`.

Para ejecutar pruebas con `pytest`, se recomienda añadir el complemento oficial:

```powershell
uv add --dev pytest-playwright
```

Las automatizaciones independientes solo necesitan `playwright`; el
complemento añade las funciones de pruebas que se explican más adelante.

## Primer ejemplo

Una automatización con la API síncrona tiene esta estructura:

```python
from playwright.sync_api import sync_playwright


with sync_playwright() as playwright:
    navegador = playwright.chromium.launch(headless=True)
    pagina = navegador.new_page()

    pagina.goto("https://example.com")
    print(pagina.title())

    navegador.close()
```

La llamada `sync_playwright()` prepara Playwright. El contexto `with` se ocupa
de liberar sus recursos cuando termina el programa.

`headless=True` ejecuta el navegador sin mostrar una ventana. Para observar lo
que ocurre durante el desarrollo se puede utilizar `headless=False`:

```python
navegador = playwright.chromium.launch(headless=False)
```

## Partes de una automatización

Los conceptos principales son:

- `Browser`: el navegador completo.
- `BrowserContext`: una sesión aislada con sus propias cookies y
  almacenamiento.
- `Page`: una pestaña abierta.
- `Locator`: una referencia para encontrar e interactuar con elementos.

El flujo habitual es crear un navegador, abrir una página, localizar elementos
y realizar acciones:

```python
from playwright.sync_api import sync_playwright


with sync_playwright() as playwright:
    navegador = playwright.chromium.launch()
    pagina = navegador.new_page()

    pagina.goto("https://example.com")
    titulo = pagina.title()

    print(titulo)
    navegador.close()
```

## Localizadores

Un localizador identifica uno o varios elementos de la página. Se recomienda
buscar por roles, nombres y textos visibles antes que por selectores CSS
complejos, porque el código queda más cercano a la forma en que una persona
utiliza la web.

```python
pagina.get_by_role("heading", name="Example Domain")
pagina.get_by_role("link", name="More information")
pagina.get_by_label("Correo electrónico")
pagina.get_by_placeholder("Escribe tu nombre")
pagina.get_by_text("Guardar")
```

Si la página utiliza atributos preparados para pruebas:

```python
pagina.get_by_test_id("boton-guardar")
```

Para crear un `data-testid`, el HTML debería contener:

```html
<button data-testid="boton-guardar">Guardar</button>
```

También se pueden utilizar selectores CSS:

```python
pagina.locator("input.email")
pagina.locator("#guardar")
```

Es preferible reservar los selectores CSS para los casos que no se puedan
expresar de una forma más estable.

## Realizar acciones

Los localizadores permiten hacer clic, escribir, seleccionar y completar
casillas:

```python
pagina.get_by_label("Nombre").fill("Ana")
pagina.get_by_label("País").select_option("ES")
pagina.get_by_label("Acepto las condiciones").check()
pagina.get_by_role("button", name="Guardar").click()
```

Al escribir se puede elegir entre:

- `fill()`: reemplaza directamente el contenido de un campo.
- `type()` o `press_sequentially()`: escribe pulsación a pulsación.

Para una navegación causada por un clic no suele ser necesario manejar la
espera manualmente. Playwright espera a que las acciones puedan realizarse y
detecta la carga producida por el navegador.

## Leer contenido

Se pueden recuperar propiedades de la página:

```python
titulo = pagina.title()
url = pagina.url
texto = pagina.get_by_role("heading").inner_text()
valor = pagina.get_by_label("Nombre").input_value()
```

Un atributo HTML se obtiene con `get_attribute()`:

```python
destino = pagina.get_by_role("link", name="Ayuda").get_attribute("href")
```

## Esperas automáticas y explícitas

Playwright espera automáticamente antes de realizar muchas acciones. Por
ejemplo, `click()` espera a que el botón esté visible y disponible.

No conviene utilizar esperas fijas como:

```python
pagina.wait_for_timeout(3000)
```

Son lentas y pueden fallar si la página responde con un tiempo diferente. Es
preferible esperar por la condición concreta:

```python
from playwright.sync_api import expect

mensaje = pagina.get_by_text("Cambios guardados")
expect(mensaje).to_be_visible()
```

También se puede esperar una navegación o una petición determinada:

```python
pagina.wait_for_url("**/perfil")
```

## Pruebas con pytest

Una prueba ejecuta una automatización y comprueba que el resultado es el
esperado. Con `pytest-playwright`, la función recibe una página preparada:

```python
import re

from playwright.sync_api import Page, expect


def test_pagina_de_inicio(page: Page):
    page.goto("https://example.com")

    expect(page).to_have_title("Example Domain")
    expect(page.get_by_role("heading")).to_have_text("Example Domain")
    expect(page.get_by_role("link", name="More information")).to_have_attribute(
        "href",
        re.compile(r"iana\.org"),
    )
```

La prueba se ejecuta desde la raíz del proyecto:

```powershell
uv run pytest
```

Para un archivo concreto:

```powershell
uv run pytest tests/test_web.py
```

Por defecto, los navegadores utilizados por el complemento pueden ejecutarse
en modo sin ventana. Para observar la ejecución:

```powershell
uv run pytest tests/test_web.py --headed
```

## Afirmaciones de Playwright

`expect()` tiene aserciones que esperan a que la condición se cumpla:

```python
from playwright.sync_api import expect

expect(pagina).to_have_url("https://example.com/")
expect(pagina).to_have_title("Example Domain")
expect(pagina.get_by_text("Bienvenido")).to_be_visible()
expect(pagina.get_by_role("button", name="Enviar")).to_be_enabled()
expect(pagina.get_by_label("Nombre")).to_have_value("Ana")
```

Si una condición no se cumple al momento, Playwright vuelve a comprobarla
durante un periodo de espera. Esto evita añadir ciclos y pausas manuales.

## Automatizaciones sin pytest

Para una tarea programada no es necesario utilizar el sistema de pruebas. Se
puede crear un script normal:

```python
from playwright.sync_api import sync_playwright


def generar_captura():
    with sync_playwright() as playwright:
        navegador = playwright.chromium.launch()
        pagina = navegador.new_page(viewport={"width": 1280, "height": 720})

        pagina.goto("https://example.com")
        pagina.screenshot(path="capturas/inicio.png", full_page=True)

        navegador.close()


if __name__ == "__main__":
    generar_captura()
```

El script se ejecuta como cualquier programa Python:

```powershell
uv run python automatizacion.py
```

Una carpeta o archivo de salida debe existir o crearse antes de guardarlo.

## Descargar archivos

Playwright permite observar una descarga producida por un clic:

```python
with pagina.expect_download() as informacion:
    pagina.get_by_role("button", name="Descargar informe").click()

descarga = informacion.value
descarga.save_as("informes/informe.pdf")
```

La aplicación remota puede usar una descarga distinta cada vez. `suggested_filename`
proporciona el nombre recomendado por el servidor:

```python
print(descarga.suggested_filename)
```

## Rellenar formularios

Un formulario puede automatizarse de forma similar a una prueba:

```python
pagina.goto("https://ejemplo.test/contacto")

pagina.get_by_label("Nombre").fill("Ana")
pagina.get_by_label("Correo electrónico").fill("ana@example.test")
pagina.get_by_label("Mensaje").fill("Quiero más información.")
pagina.get_by_role("button", name="Enviar").click()

from playwright.sync_api import expect

expect(pagina.get_by_text("Mensaje enviado")).to_be_visible()
```

Las direcciones `ejemplo.test` del código sirven para explicar el ejemplo. Para
ejecutarlo de verdad, hay que sustituirlas por la URL de una aplicación
disponible.

## Sesiones e inicio de sesión

Se puede introducir una cuenta para la prueba:

```python
pagina.goto("https://aplicacion.example/login")

pagina.get_by_label("Usuario").fill("usuario_de_prueba")
pagina.get_by_label("Contraseña").fill("clave_de_prueba")
pagina.get_by_role("button", name="Entrar").click()

pagina.wait_for_url("**/inicio")
```

Las credenciales reales nunca deben escribirse directamente en el código ni
subirse a Git. Deben utilizarse cuentas de prueba y variables de entorno o un
gestor de secretos.

## Reutilizar una sesión

Un contexto puede guardar cookies y datos de almacenamiento:

```python
contexto.storage_state(path="estado-login.json")
```

La sesión puede cargarse en otro contexto:

```python
contexto = navegador.new_context(storage_state="estado-login.json")
pagina = contexto.new_page()
```

El archivo puede incluir datos sensibles. No debe añadirse al repositorio. En
pruebas conviene autenticar una vez por cada sesión controlada y limpiar los
datos cuando sea necesario.

## API síncrona y asíncrona

Esta guía utiliza la API síncrona, adecuada para programas y pruebas sencillas.
Playwright también ofrece una API asíncrona:

```python
import asyncio

from playwright.async_api import async_playwright


async def principal():
    async with async_playwright() as playwright:
        navegador = await playwright.chromium.launch()
        pagina = await navegador.new_page()
        await pagina.goto("https://example.com")
        print(await pagina.title())
        await navegador.close()


asyncio.run(principal())
```

No se deben mezclar las API síncrona y asíncrona dentro del mismo flujo. Se
elige la asíncrona cuando el resto de la aplicación ya utiliza `asyncio`.

## Diferencias entre pruebas y automatizaciones

| Prueba | Automatización |
| --- | --- |
| Comprueba un resultado esperado | Completa una tarea |
| Debe fallar si aparece una regresión | Puede generar archivos o datos |
| Se ejecuta normalmente con `pytest` | Puede ejecutarse manualmente o de forma programada |
| Busca resultados repetibles y aislados | Puede depender de un servicio externo |
| Protege el comportamiento de la aplicación | Ahorrar trabajo operativo |

Las aserciones con `expect()` son habituales en pruebas. En una automatización
también pueden emplearse para comprobar que una operación sensible terminó
antes de continuar.

## Buenas prácticas

### Utilizar cuentas y datos de prueba

Una automatización no debe borrar ni modificar datos reales por accidente.
Cuando sea posible, usa una página de pruebas con datos aislados.

### Mantener localizadores estables

Prioriza roles, etiquetas y atributos de prueba frente a clases o rutas de CSS
que cambien frecuentemente.

### Evitar esperas fijas

Espera una condición observable, como la presencia de un mensaje, una URL o un
botón habilitado.

### Aislar cada prueba

Cada prueba debe poder ejecutarse de forma independiente. `pytest-playwright`
crea contextos limpios, lo que evita compartir cookies y almacenamiento entre
pruebas.

### Guardar una traza cuando falle una prueba

Las trazas ayudan a investigar los pasos realizados:

```powershell
uv run pytest --tracing=retain-on-failure
```

La traza puede visualizarse con:

```powershell
uv run playwright show-trace test-results/ruta-de-la-traza.zip
```

También se puede crear una captura al detectar un error:

```python
pagina.screenshot(path="error.png", full_page=True)
```

Las capturas y trazas no deben sustituir a un mensaje claro sobre el fallo.

## Errores habituales

### No instalar el navegador

La instalación del paquete Python no incluye necesariamente un ejecutable del
navegador. Después de instalar Playwright, ejecuta `playwright install`.

### Usar selectores frágiles

Una ruta CSS como `div > div > span:nth-child(3)` puede romperse al cambiar el
diseño. Busca el elemento por su etiqueta, rol o texto.

### Añadir pausas manuales

Las pausas fijas ralentizan pruebas y automatizaciones. Espera una condición
con `expect()` o con uno de los métodos `wait_for_*`.

### Compartir credenciales

Las credenciales, cookies y estados de inicio de sesión contienen información
sensible. No se deben incluir en código, capturas públicas ni trazas compartidas.

### Automatizar sitios sin autorización

Solo se debe automatizar un sitio cuando se tiene permiso, se respetan sus
condiciones de uso y se evita sobrecargarlo con peticiones.

## Ejercicio

Construye una prueba para una página de inicio:

1. Abre una dirección de una aplicación de prueba.
2. Comprueba el título de la página con `expect(page).to_have_title(...)`.
3. Localiza un enlace por su rol y comprueba su atributo `href`.
4. Haz clic en el enlace.
5. Espera a que cambie la URL o aparezca un encabezado.
6. Ejecuta la prueba con `pytest`.

Como extensión, crea un script independiente que abra la misma página y guarde
una captura de pantalla completa.
