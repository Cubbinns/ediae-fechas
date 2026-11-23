import pytest

from app.utils import create_folder_if_not_exists

def test_create_folder_if_not_exists(tmp_path):
    folder_path = tmp_path / "test_folder"
    create_folder_if_not_exists(folder_path)
    assert folder_path.exists() and folder_path.is_dir()

    # Test creating the folder again should not raise an error
    create_folder_if_not_exists(folder_path)
    assert folder_path.exists() and folder_path.is_dir()