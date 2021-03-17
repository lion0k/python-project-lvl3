"""Test file."""

import tempfile
from os import chmod
from os.path import join

import pytest
from page_loader.file import create_directory, write_file
from page_loader.logging import KnownError

PERMISSION_ONLY_READ = 0o444


def test_raises_exception_create_directory():
    """
    Test raise exception when create directory.

    check raises OSError, PermissionError
    """
    with tempfile.TemporaryDirectory() as tempdir:
        create_directory(tempdir, 'test')
        with pytest.raises(KnownError):
            create_directory(tempdir, 'test')

        chmod(tempdir, PERMISSION_ONLY_READ)
        with pytest.raises(KnownError):
            create_directory(tempdir, 'another_folder')


def test_raises_exception_write_file():
    """
    Test raise exception when write file.

    check raises OSError, PermissionError
    """
    with tempfile.TemporaryDirectory() as tempdir:
        path_fake_folder = join(tempdir, 'test_file')
        write_file(path_fake_folder, b'data')
        with pytest.raises(KnownError):
            write_file(join(path_fake_folder, 'test'), '')

        chmod(tempdir, PERMISSION_ONLY_READ)
        with pytest.raises(KnownError):
            write_file(join(tempdir, 'file'), b'data')
