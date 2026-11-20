from typer import Typer
from loguru import logger

from app.configuration.config import FechasConfig
from app.datafiles.jsondatafile import JsonDatafile
from app.models.almacen import Almacen
from app.models.usuario import Usuario

cli = Typer()
usuarios = Typer()
cli.add_typer(usuarios, name="usuarios")
configuration = Typer()
cli.add_typer(configuration, name="configuration")

@usuarios.command()
def list():
    """
    List all users in the application.
    """
    config = FechasConfig()
    datafile = JsonDatafile(config.get_data_file_path())
    if datafile.it_exists():
        almacen: Almacen | None = datafile.read()
        if almacen is None:
            logger.error("Failed to read almacen from JSON data file.")
            exit(-1)
        for usuario in almacen.usuarios:
            print(usuario.username)
    else:
        logger.info("No users found.")

@usuarios.command()
def create(username: str):
    """
    Create a new username for the application.

    Args:
        username (str): The username for the new configuration.
    """
    config = FechasConfig()
    datafile = JsonDatafile(config.get_data_file_path())
    if datafile.it_exists():
        almacen: Almacen | None = datafile.read()
        if almacen is None:
            logger.error("Failed to read almacen from JSON data file.")
            exit(-1)
        if almacen.usuario_exists(username):
            logger.error("User with username '{}' already exists.", username)
            exit(-1)
        almacen.usuarios.append(Usuario(username=username))
        datafile.write(almacen)
        logger.info("User with username '{}' has been added.", username)
    else:
        almacen: Almacen = Almacen(usuarios=[Usuario(username=username)])
        datafile.write(almacen)
        logger.info("User with username '{}' has been added.", username)

@configuration.command()
def show():
    """
    Show the current configuration of the application.
    """
    from app.configuration.config import FechasConfig
    config = FechasConfig()
    print("Data folder:", config.get_data_folder())
    print("Data file name:", config.get_data_file_name())
    print("Data file format:", config.get_data_file_format())

