"""File functions."""

from os import mkdir
from os.path import isdir, join, split, splitext
from re import sub

DIR_EXIST_ERROR = "\nDirectory already exist '{path}'"
PATH_ERROR = "\nDirectory under the given path '{path}' not found"
PERMISSION_ERROR = "\nNo permission to write. Path '{path}'"


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
    except PermissionError:
        raise PermissionError(PERMISSION_ERROR.format(path=abs_path))
    except OSError:
        raise OSError(DIR_EXIST_ERROR.format(path=abs_path))

    return abs_path


def write_file(path: str, data, binary=False):
    """
    Write file.

    Args:
        path: full path
        data: data
        binary: binary data

    Raises:
        OSError: directory not exists
        PermissionError: not permission to write
    """
    directory, _ = split(path)

    if not isdir(directory):
        raise OSError(PATH_ERROR.format(path=directory))

    mode = 'wb' if binary else 'w'
    try:
        with open(path, mode) as file_descriptor:
            file_descriptor.write(data)
    except PermissionError:
        raise PermissionError(PERMISSION_ERROR.format(path=path))


def convert_name(url: str, parse_extension=False) -> str:
    """
    Convert name.

    Args:
        url: URL
        parse_extension: parse extension

    Returns:
        str:
    """
    url_without_scheme = sub('(^.+://)', '', url)
    if parse_extension:
        path, extension = splitext(url_without_scheme)
        return '{name}{extension}'.format(
            name=sub('([^a-zA-Z0-9]+)', '-', path),
            extension=extension,
        )
    return '{name}'.format(
        name=sub('([^a-zA-Z0-9]+)', '-', url_without_scheme),
    )
