# ediae-fechas

Ejercicio de consola para practicar fechas, clases y archivos. Permite guardar
usuarios y consultar o mostrar la configuración de la aplicación.

## Requisitos

- Windows, Linux o macOS.
- [uv](https://docs.astral.sh/uv/) instalado.
- El proyecto requiere Python 3.14 o superior.

No es necesario crear manualmente un entorno virtual ni activar ninguna
versión de Python: `uv` puede instalar y gestionar ambas cosas.

## Instalación

1. Clona el repositorio y entra en el directorio del proyecto:

   ```powershell
   git clone https://github.com/Kalebros/ediae-fechas.git
   cd ediae-fechas
   ```

2. Instala Python y las dependencias definidas en `pyproject.toml`:

   ```powershell
   uv python install 3.14
   uv sync
   ```

   Para comprobar que `uv` ha preparado el entorno:

   ```powershell
   uv run python --version
   ```

## Configuración

La configuración se encuentra en `configurations/default.yaml`:

```yaml
data_folder: C:\ruta\al\proyecto\data
data_file:
  name: data.json
  format: json
```

Antes de usar el programa, ajusta `data_folder` para que apunte a la carpeta
`data` de tu copia del proyecto. Utiliza una ruta absoluta. Por ejemplo, en
Windows puede tener este aspecto:

```yaml
data_folder: C:\Workbench\python\master_ediae_2027\ediae-fechas\data
```

Los usuarios se almacenan en el archivo indicado por esa ruta, normalmente
`data/data.json`.

## Lanzar la aplicación

Desde la raíz del proyecto ejecuta:

```powershell
uv run python main.py --help
```

La ayuda muestra los grupos de comandos disponibles:

- `usuarios`: gestión de usuarios.
- `configuration`: consulta de la configuración.

También se puede llamar directamente al módulo de línea de comandos:

```powershell
uv run python main.py usuarios --help
uv run python main.py configuration --help
```

## Uso

### Consultar la configuración

```powershell
uv run python main.py configuration show
```

Muestra la carpeta de datos, el nombre del archivo y su formato.

### Crear un usuario

```powershell
uv run python main.py usuarios create "Nombre Apellidos"
```

La aplicación añade el usuario al archivo JSON. Si el archivo no existe, crea
primero el almacenamiento completo. Si ya existe un usuario con ese nombre,
termina con un error.

Ejemplo:

```powershell
uv run python main.py usuarios create "Antonio Ramírez"
```

### Listar los usuarios

```powershell
uv run python main.py usuarios list
```

Cada nombre se imprime en una línea. Si todavía no existe el archivo de datos,
la aplicación informa de que no hay usuarios.

### Datos generados

Los datos tienen esta estructura:

```json
{
  "usuarios": [
    {
      "username": "Antonio Ramírez",
      "vacaciones": []
    }
  ]
}
```

Se recomienda modificar la configuración y los datos con cuidado. Los modelos
Pydantic validarían la estructura al cargar el archivo.

## Desarrollo

### Ejecutar las comprobaciones

El proyecto incluye `pytest` como dependencia de desarrollo:

```powershell
uv run pytest
```

### Dónde estudiar cada librería

Hay una guía breve por dependencia en la carpeta [doc](doc):

- [Typer](doc/typer.md)
- [Arrow](doc/arrow.md)
- [simplejson](doc/simplejson.md)
- [Pydantic](doc/pydantic.md)
- [OmegaConf](doc/omegaconf.md)
- [Clases abstractas, herencia y polimorfismo](doc/clases-abstractas.md)
- [Date y datetime](doc/date-datetime.md)
- [Decimal](doc/decimal.md)
