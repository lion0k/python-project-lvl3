"""Test page loader."""

import tempfile
from os.path import abspath, dirname, join, sep

import requests_mock
from page_loader import download
from page_loader.engine import parse_page, send_request

ABSOLUTE_PATH_FIXTURE_DIR = '{abs_path}{sep}{dir_fixtures}{sep}'.format(
    abs_path=abspath(dirname(__file__)),
    sep=sep,
    dir_fixtures='fixtures',
)
URL = 'http://test.com'


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
    with requests_mock.Mocker() as mock:
        mock.get(URL, text='data')
        with tempfile.TemporaryDirectory() as tempdir:
            expected = join(tempdir, 'test-com.html')
            assert expected == download(tempdir, URL)


def test_parse_page():
    """Test parse page."""
    with open(get_file_absolute_path('page.html')) as file_before:
        parsed_page_before = file_before.read()
        with requests_mock.Mocker() as mock:
            mock.get(URL, text=parsed_page_before)
            with open(get_file_absolute_path('expected.html')) as file_after:
                parsed_page_after = file_after.read()
                assert parsed_page_after == parse_page(
                    send_request(URL).data,
                    URL,
                    'test',
                )[0]
