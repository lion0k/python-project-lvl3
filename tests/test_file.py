"""Test file."""

import os
import tempfile
from urllib.parse import urljoin

import pytest
from page_loader.file import (
    MAX_LENGTH_FILENAME,
    build_filename,
    create_directory,
    write_file,
)

PERMISSION_ONLY_READ = 0o444


def test_raises_exception_create_directory():
    """
    Test raise exception when create directory.

    check raises OSError, PermissionError
    """
    with tempfile.TemporaryDirectory() as tempdir:
        create_directory(tempdir, 'test')
        with pytest.raises(OSError):
            create_directory(tempdir, 'test')

        os.chmod(tempdir, PERMISSION_ONLY_READ)
        with pytest.raises(PermissionError):
            create_directory(tempdir, 'another_folder')


def test_raises_exception_write_file():
    """
    Test raise exception when write file.

    check raises OSError, PermissionError
    """
    with tempfile.TemporaryDirectory() as tempdir:
        path_fake_folder = os.path.join(tempdir, 'test_file')
        write_file(path_fake_folder, b'data')
        with pytest.raises(OSError):
            write_file(os.path.join(path_fake_folder, 'test'), '')

        os.chmod(tempdir, PERMISSION_ONLY_READ)
        with pytest.raises(PermissionError):
            write_file(os.path.join(tempdir, 'file'), b'data')


@pytest.mark.parametrize(
    'root_url, src_url, expected', [
        (
            'http://test.com/test',
            'images/python.png',
            'test-com-images-python.png',
        ),
        (
            'http://test.com/test',
            '//test.com/images/python.png',
            'test-com-images-python.png',
        ),
        ('http://127.0.0.1', '/test', '127-0-0-1-test.html'),
        ('http://127.0.0.1', '', '127-0-0-1.html'),
    ],
)
def test_build_filename(root_url, src_url, expected):
    """
    Check build filename.

    Args:
        root_url: root URL
        src_url:  source URL
        expected: expected filename
    """
    assert build_filename(urljoin(root_url, src_url)) == expected


def test_limit_length_build_filename():
    """Check limit length build filename."""
    root_url = 'http://127.0.0.1'
    expected = MAX_LENGTH_FILENAME
    over_length_filename = MAX_LENGTH_FILENAME + 50
    expected_extension = '.png2png'
    gen_name = ''.join(['a' for _ in range(over_length_filename)])
    name_without_exp = '/{name}'.format(name=gen_name)
    name_with_exp = '/{name}{extension}'.format(
        name=gen_name,
        extension=expected_extension,
    )
    filename_with_extension = build_filename(urljoin(root_url, name_with_exp))
    extension = os.path.splitext(filename_with_extension)[1]
    assert len(build_filename(urljoin(root_url, name_without_exp))) == expected
    assert len(filename_with_extension) == expected
    assert extension == expected_extension
