# Pydantic: modelos y validación

Pydantic permite describir la forma de los datos mediante clases. El proyecto
usa Pydantic para representar usuarios y el almacenamiento de la aplicación.

## Modelo básico

En `app/models/usuario.py`:

```python
from pydantic import BaseModel, Field
from datetime import date
from typing import List

class Usuario(BaseModel):
    username: str
    vacaciones: List[date] = Field(default_factory=list)
```

Cada instancia debe tener un `username` de tipo `str`. `vacaciones` es una
lista de objetos `date` y su valor predeterminado es una lista nueva por cada
usuario.

Se crea así:

```python
usuario = Usuario(username="Ana")
print(usuario.username)
print(usuario.vacaciones)
```

## Validación automática

Pydantic intenta convertir o validar los valores recibidos:

```python
usuario = Usuario(username="Ana", vacaciones=["2027-07-01"])
print(usuario.vacaciones)
# [datetime.date(2027, 7, 1)]
```

Si el dato no puede convertirse a la estructura definida, Pydantic lanza una
excepción `ValidationError`.

## Modelos anidados

`app/models/almacen.py` contiene una lista de usuarios:

```python
from pydantic import BaseModel

class Almacen(BaseModel):
    usuarios: List[Usuario]
```

Al construir `Almacen(**diccionario)`, Pydantic crea instancias de `Usuario`
para cada elemento de la lista.

## Leer JSON con Pydantic

El flujo usado por el proyecto es:

```python
datos = json.load(archivo)
almacen = Almacen(**datos)
```

Es una combinación útil: simplejson obtiene los datos básicos y Pydantic
convierte esa información en objetos comprobados.

## Convertir el modelo

Antes de guardar:

```python
almacen.model_dump()
```

devuelve un diccionario o una estructura compatible con JSON.

`model_dump_json()` devuelve directamente una cadena JSON, aunque este proyecto
utiliza `model_dump()` junto con simplejson para conservar el control sobre
la escritura.

## Comprobar datos

Cuando un valor no pertenece al modelo:

```python
from pydantic import ValidationError

try:
    usuario = Usuario(username=123)
except ValidationError as error:
    print(error)
```

Pydantic puede convertir algunos valores compatibles. Por eso conviene también
validar la entrada de un usuario antes de modificar el archivo.

## Ejercicio

1. Crea un `Usuario` sin vacaciones.
2. Crea otro con una fecha como texto.
3. Construye un `Almacen` con ambos.
4. Convierte el resultado con `model_dump()` y muestra el diccionario.
