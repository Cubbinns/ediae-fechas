# Typer: comandos de consola

Typer permite convertir funciones de Python en una aplicación de línea de
comandos (CLI). Se usa en `app/cli.py`.

## Conceptos principales

`Typer()` crea la aplicación raíz. Una segunda instancia puede representar un
grupo de comandos:

```python
from typer import Typer

cli = Typer()
usuarios = Typer()
cli.add_typer(usuarios, name="usuarios")
```

Aquí `usuarios` se registra debajo de `cli`, por lo que sus comandos empiezan
por `usuarios`.

Decorar una función con `@usuarios.command()` la convierte en una subacción:

```python
@usuarios.command()
def list():
    print("Sin usuarios")
```

El nombre de la función determina el nombre del comando. Por eso `list()` se
ejecuta como `usuarios list`.

## Argumentos

Typer crea argumentos y opciones a partir de las anotaciones de tipos:

```python
@usuarios.command()
def create(username: str):
    print(username)
```

`username: str` se interpreta como un argumento obligatorio:

```powershell
uv run python main.py usuarios create "Ana Pérez"
```

Una anotación como `opcion: bool = False` se puede convertir en una opción
booleana. Typer también genera ayuda a partir de los docstrings y las
anotaciones.

## Punto de entrada

En `main.py` se importa la aplicación y se invoca:

```python
from app.cli import cli

cli()
```

Este patrón permite lanzar el programa con `python main.py`.

## Comandos útiles

```powershell
uv run python main.py --help
uv run python main.py usuarios --help
uv run python main.py usuarios create --help
```

Typer usa el nombre `list` para el comando, aunque `list` también sea una
función integrada de Python. En este proyecto no hay un problema en concreto,
pero conviene evitar nombres que resulten confusos en otros programas.

## Ejercicio

1. Añade un comando `configuration show`.
2. Prueba qué ocurre al ejecutar `--help`.
3. Añade un argumento opcional con un valor predeterminado.
4. Comprueba que Typer comprueba que el argumento obligatorio esté presente.
