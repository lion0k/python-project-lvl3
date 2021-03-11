"""Page loader engine."""

from os.path import isdir, join, split
from re import sub

from page_loader.request import send_request

PATH_ERROR = "\nDirectory under the given path '{path}' not found"
PERMISSION_ERROR = "\nNo permission to write the file. Path '{path}'"


def download(output_dir: str, url: str) -> str:
    """
    Download file from URL.

    Args:
        output_dir: directory to download
        url: URL

    Returns:
        str:
    """
    response = send_request(url)
    path = join(output_dir, set_filename(url))
    write_file(path, response)
    return path


def write_file(path: str, data):
    """
    Write file.

    Args:
        path: path
        data: data

    Raises:
        OSError: directory not exists
        PermissionError: not permission to write
    """
    directory, _ = split(path)

    if not isdir(directory):
        raise OSError(PATH_ERROR.format(path=directory))

    try:
        with open(path, 'wb') as file_descriptor:
            file_descriptor.write(data)
    except PermissionError:
        raise PermissionError(PERMISSION_ERROR.format(path=path))


def set_filename(url: str) -> str:
    """
    Build filename.

    Args:
        url: URL

    Returns:
        str: filename
    """
    url_without_scheme = sub('(^.+://)', '', url)
    filename = sub('([^a-zA-Z0-9]+)', '-', url_without_scheme)
    return '{filename}.html'.format(filename=filename)
