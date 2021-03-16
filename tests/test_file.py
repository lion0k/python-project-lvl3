"""Test file."""

import tempfile
from os import chmod
from os.path import join

import pytest
from page_loader.file import create_directory, write_file

PERMISSION_ONLY_READ = 0o444


def test_raises_exception_create_directory():
    """Test raise exception when create directory."""
    with tempfile.TemporaryDirectory() as tempdir:
        create_directory(tempdir, 'test')
        with pytest.raises(OSError):
            create_directory(tempdir, 'test')

        chmod(tempdir, PERMISSION_ONLY_READ)
        with pytest.raises(PermissionError):
            create_directory(tempdir, 'another_folder')


def test_raises_exception_write_file():
    """Test raise exception when write file."""
    with tempfile.TemporaryDirectory() as tempdir:
        path_fake_folder = join(tempdir, 'test_file')
        write_file(path_fake_folder, 'data')
        with pytest.raises(OSError):
            write_file(join(path_fake_folder, 'test'), '')

        chmod(tempdir, PERMISSION_ONLY_READ)
        with pytest.raises(PermissionError):
            write_file(join(tempdir, 'file'), 'data')
