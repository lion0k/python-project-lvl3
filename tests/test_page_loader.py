"""Test page loader."""

import tempfile
from os.path import abspath, dirname, join, sep

import requests_mock
from page_loader import download

ABSOLUTE_PATH_FIXTURE_DIR = '{abs_path}{sep}{dir_fixtures}{sep}'.format(
    abs_path=abspath(dirname(__file__)),
    sep=sep,
    dir_fixtures='fixtures',
)


def get_file_absolute_path(filename: str) -> str:
    """
    Get absolute path file in directory fixtures.

    Args:
        filename: file name

    Returns:
        str:
    """
    return '{abs_path}{filename}'.format(
        abs_path=ABSOLUTE_PATH_FIXTURE_DIR,
        filename=filename,
    )


def test_page_loader():
    """Test page loader."""
    url = 'http://test.com'
    with requests_mock.Mocker() as mock:
        mock.get(url, text='data')
        with tempfile.TemporaryDirectory() as tempdir:
            expected = join(tempdir, 'test-com.html')
            assert expected == download(tempdir, url)
