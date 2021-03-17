"""File functions."""

import logging
from os import mkdir
from os.path import isdir, join, split

from page_loader.logging import KnownError

PATH_ERROR = "Directory under the given path '{path}' not found"


def create_directory(path: str, name_folder: str) -> str:
    """
    Create directory.

    Args:
        path: full path
        name_folder: name folder

    Raises:
        KnownError: OSError, PermissionError

    Returns:
        str: full path to created directory
    """
    abs_path = join(path, name_folder)
    try:
        mkdir(abs_path)
    except PermissionError as error:
        logging.error(error)
        raise KnownError(error)
    except OSError as error:
        logging.error(error)
        raise KnownError(error)

    logging.debug('Successful create directory {path}'.format(
        path=abs_path,
    ))
    return abs_path


def write_file(path: str, data):
    """
    Write file.

    Args:
        path: full path
        data: data

    Raises:
        KnownError: OSError, PermissionError
    """
    directory, _ = split(path)

    if not isdir(directory):
        logging.error(PATH_ERROR.format(path=directory))
        raise KnownError(PATH_ERROR.format(path=directory))

    try:
        with open(path, 'wb') as file_descriptor:
            file_descriptor.write(data)
    except PermissionError as error:
        logging.error(error)
        raise KnownError(error)

    logging.debug('Successful write file {path}'.format(
        path=path,
    ))
