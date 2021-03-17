"""File functions."""

import logging
from os import mkdir
from os.path import isdir, join, split

DIR_EXIST_ERROR = "Directory already exist '{path}'"
PATH_ERROR = "Directory under the given path '{path}' not found"
PERMISSION_ERROR = "No permission to write. Path '{path}'"


def create_directory(path: str, name_folder: str) -> str:
    """
    Create directory.

    Args:
        path: full path
        name_folder: name folder

    Raises:
        OSError: directory already exist
        PermissionError: not permission to write

    Returns:
        str: full path to created directory
    """
    abs_path = join(path, name_folder)
    try:
        mkdir(abs_path)
    except PermissionError as error:
        logging.error(error)
        raise PermissionError(PERMISSION_ERROR.format(path=abs_path))
    except OSError as error:
        logging.error(error)
        raise OSError(DIR_EXIST_ERROR.format(path=abs_path))

    return abs_path


def write_file(path: str, data):
    """
    Write file.

    Args:
        path: full path
        data: data

    Raises:
        OSError: directory not exists
        PermissionError: not permission to write
    """
    directory, _ = split(path)

    if not isdir(directory):
        logging.error(PATH_ERROR.format(path=directory))
        raise OSError(PATH_ERROR.format(path=directory))

    try:
        with open(path, 'wb') as file_descriptor:
            file_descriptor.write(data)
    except PermissionError as error:
        logging.error(error)
        raise PermissionError(PERMISSION_ERROR.format(path=path))
