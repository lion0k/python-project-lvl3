"""Test page loader."""

import tempfile
from os.path import abspath, dirname, isdir, isfile, join, sep

import requests_mock
from page_loader import download

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
    with tempfile.TemporaryDirectory() as tempdir:
        expected_path_index_page = join(tempdir, 'test-com.html')
        with open(get_file_absolute_path('page.html')) as file_before:
            with requests_mock.Mocker() as mock:
                mock.get(URL, text=file_before.read())
                mock.get('http://test.com/images/python.png', content=b'png')
                mock.get('http://test.com/scripts/test.js', content=b'js')
                mock.get('http://test.com/courses', content=b'html')
                mock.get('http://test.com/styles/app.css', content=b'css')
                assert expected_path_index_page == download(URL, tempdir)
                resources_dir = join(tempdir, 'test-com_files')
                assert isdir(resources_dir)
                expected_files = [
                    'test-com-images-python.png',
                    'test-com-courses.html',
                    'test-com-scripts-test.js',
                    'test-com-styles-app.css',
                ]
                for filename in expected_files:
                    assert isfile(join(resources_dir, filename))
