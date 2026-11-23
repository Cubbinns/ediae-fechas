import os
from loguru import logger

def create_folder_if_not_exists(folder_path):
    """
    Create the folder at the specified path if it does not already exist.

    Args:
        folder_path (str): The path of the folder to create if it does not exist.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logger.info("Created folder at '{}'.", folder_path)
    else:
        logger.info("Folder already exists at '{}'.", folder_path)

