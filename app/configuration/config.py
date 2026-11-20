from omegaconf import OmegaConf
from pathlib import Path

from app.constants import CONFIGURATION_PATH


class FechasConfig:
    """
    Configuration class for the Fechas application.
    Loads and provides access to the application's configuration.
    """

    _configuration_path: Path = CONFIGURATION_PATH # Default configuration file path

    @classmethod
    def get_configuration_path(cls) -> Path:
        """
        Returns the current configuration file path.

        Returns:
            Path: The current configuration file path.
        """
        return cls._configuration_path

    @classmethod
    def set_configuration_path(cls, path: Path):
        """
        Sets the configuration file path.

        Args:
            path (Path): The new configuration file path.
        """
        cls._configuration_path = path


    def __init__(self):
        """
        Initializes the FechasConfig instance by loading the configuration from the current configuration file path.

        """
        self.config = OmegaConf.load(self._configuration_path)

    def get_data_folder(self) -> str:
        """
        Returns the data folder path from the configuration.

        Returns:
            str: The data folder path.
        """
        return self.config.data_folder

    def get_data_file_path(self) -> Path:
        """
        Returns the full path to the data file.

        Returns:
            Path: The full path to the data file.
        """
        return Path(self.get_data_folder()) / self.get_data_file_name()

    def get_data_file(self) -> dict:
        """
        Returns the data file configuration as a dictionary.

        Returns:
            dict: The data file configuration.
        """
        return self.config.data_file

    def get_data_file_name(self) -> str:
        """
        Returns the name of the data file from the configuration.

        Returns:
            str: The data file name.
        """
        return self.config.data_file.name

    def get_data_file_format(self) -> str:
        """
        Returns the format of the data file from the configuration.

        Returns:
            str: The data file format.
        """
        return self.config.data_file.format