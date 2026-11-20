# simplejson: leer y escribir JSON

simplejson es compatible con gran parte de la API de la biblioteca estándar
`json`, pero incluye características adicionales. El proyecto importa:

```python
import simplejson as json
```

Esto permite usar `json.load()` y `json.dump()` casi igual que con `json`
de Python. Se utiliza en `app/datafiles/jsondatafile.py`.

## Leer JSON

```python
import simplejson as json

with open("data/data.json", "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)
```

`datos` será una estructura formada por diccionarios y listas.

En el proyecto se utiliza `datos` para construir un modelo Pydantic:

```python
return Almacen(**json.load(f))
```

Las claves del diccionario deben coincidir con los campos del modelo.

## Escribir JSON

```python
import simplejson as json

datos = {"usuarios": []}

with open("data/data.json", "w", encoding="utf-8") as archivo:
    json.dump(datos, archivo, ensure_ascii=False)
```

`ensure_ascii=False` mantiene caracteres como `á`, `ñ` o `ó` en lugar de
codificarlos como secuencias ASCII.

El proyecto primero convierte el modelo Pydantic a un diccionario:

```python
almacen_dump = almacen.model_dump()
json.dump(almacen_dump, f, ensure_ascii=False)
```

## Errores comunes

La clase `JsonDatafile` contempla dos problemas habituales:

- `FileNotFoundError`: el archivo todavía no existe.
- `json.JSONDecodeError`: el contenido no tiene JSON válido.

Siempre conviene indicar al usuario qué ha fallado y no continuar como si
la lectura hubiera tenido éxito.

## Archivos y rutas

Usar `Path` permite trabajar con rutas de forma clara:

```python
from pathlib import Path

ruta = Path("data") / "data.json"
```

La ruta también puede detectar si existe:

```python
ruta.exists()
```

## Ejercicio

Lee `data/data.json`, muestra el número de usuarios e identifica los campos
que contiene el primer usuario. Después escribe una lista con los nombres
sin modificar el archivo original.
