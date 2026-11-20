# OmegaConf: configuración en YAML

OmegaConf carga y administra configuraciones estructuradas. El proyecto utiliza
YAML en `configurations/default.yaml` y OmegaConf en
`app/configuration/config.py`.

## Archivo de configuración

```yaml
data_folder: C:\ruta\al\proyecto\data
data_file:
  name: data.json
  format: json
```

El archivo contiene dos tipos de información:

- `data_folder`: carpeta donde se guarda el archivo.
- `data_file`: objeto con nombre y formato del archivo.

## Cargar una configuración

```python
from omegaconf import OmegaConf

config = OmegaConf.load("configurations/default.yaml")
print(config.data_folder)
print(config.data_file.name)
```

OmegaConf permite acceder mediante atributos o mediante claves:

```python
print(config["data_folder"])
print(config["data_file"]["name"])
```

Ambas formas son válidas.

## Clase `FechasConfig`

La aplicación encapsula OmegaConf en `FechasConfig`:

```python
config = FechasConfig()
print(config.get_data_file_name())
print(config.get_data_file_format())
```

Esto mantiene separada la carga del archivo de la lógica de otros comandos.

La ubicación predeterminada se define en `app/constants.py`:

```python
CONFIGURATION_PATH = Path(__file__).parent / ".." / "configurations" / "default.yaml"
```

La clase puede cambiar temporalmente esa ruta:

```python
from pathlib import Path

FechasConfig.set_configuration_path(
    Path("otra-configuracion.yaml")
)
```

## Crear una configuración en Python

OmegaConf también puede crear configuraciones desde estructuras Python:

```python
from omegaconf import OmegaConf

config = OmegaConf.create({
    "data_folder": "data",
    "data_file": {
        "name": "data.json",
        "format": "json",
    },
})
```

## Ruta del archivo de datos

`get_data_file_path()` combina la carpeta y el nombre:

```python
from pathlib import Path

ruta = Path(config.get_data_folder()) / config.get_data_file_name()
```

Si el archivo cambia de nombre o ubicación, estos métodos siguen mostrando
el origen configurado.

## Precauciones

- Revisa `data_folder`: es una ruta específica del equipo donde se creó el
  proyecto.
- Cuando uses barras de ruta en YAML, prueba primero una ruta absoluta.
- Mantén las claves alineadas con los métodos de `FechasConfig`.
- No guardes contraseñas o tokens en este archivo si el repositorio es público.

## Ejercicio

1. Cambia temporalmente `data_file.name` a `ejemplo.json`.
2. Crea una instancia de `FechasConfig`.
3. Comprueba con `get_data_file_path()` la ruta completa obtenida.
