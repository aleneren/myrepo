import os, tempfile
from werkzeug.datastructures import FileStorage


def save_temporary_file(file: FileStorage, unique_filename: str) -> str:
    """
    Saves an uploaded file to a temporary location.

    Args:
        file: The uploaded file object.
        unique_filename (str): The unique filename to save as.

    Returns:
        str: The path to the saved temporary file.
    """
    tmp_dir = tempfile.gettempdir()
    tmp_path = os.path.join(tmp_dir, unique_filename)
    file.save(tmp_path)
    return tmp_path


def delete_temporary_file(file_path: str) -> bool:
    """
    Deletes a temporary file if it exists.

    Args:
        file_path (str): The path to the temporary file to delete.

    Returns:
        bool: True if the file was deleted, False otherwise.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    
    return False
