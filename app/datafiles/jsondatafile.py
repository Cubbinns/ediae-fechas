import simplejson as json
from pathlib import Path
from loguru import logger

from app.models.almacen import Almacen

class JsonDatafile:
    """
    Class for handling JSON data files.
    """
    def __init__(self, file_path: Path):
        """
        Initialize the JsonDatafile with the given file path.

        Args:
            file_path (Path): The path to the JSON data file.
        """
        self.file_path = file_path

    def it_exists(self) -> bool:
        """
        Check if the JSON data file exists.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        return self.file_path.exists()

    def read(self) -> Almacen | None:
        """
        Read the JSON data file and return an Almacen instance.

        Returns:
            Almacen | None: The Almacen instance created from the JSON data, or None if an error occurred.
        """
        try:
            with self.file_path.open("r",encoding="utf-8") as f:
                return Almacen(**json.load(f))
        except FileNotFoundError:
            logger.warning("JSON file not found: {}", self.file_path)
            return None
        except json.JSONDecodeError:
            logger.warning("JSON decode error in file: {}", self.file_path)
            return None 

    def write(self, almacen: Almacen):
        """
        Write the Almacen instance to the JSON data file.

        Args:
            almacen (Almacen): The Almacen instance to write to the file.
        """
        almacen_dump = almacen.model_dump()
        with self.file_path.open("w",encoding="utf-8") as f:
            json.dump(almacen_dump, f, ensure_ascii=False)

