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
                long_name = ''.join(['a' for _ in range(250)])
                file_a = '{url}/images/{name}a.png'.format(
                    url=URL,
                    name=long_name,
                )
                file_b = '{url}/images/{name}b.png'.format(
                    url=URL,
                    name=long_name,
                )
                file_c = '{url}/images/{name}c.png'.format(
                    url=URL,
                    name=long_name,
                )

                mock.get(URL, text=file_before.read())
                mock.get(file_a, content=b'png')
                mock.get(file_b, content=b'png')
                mock.get(file_c, content=b'png')
                mock.get('{url}/images/python.png'.format(url=URL), content=b'png')
                mock.get('{url}/scripts/test.js'.format(url=URL), content=b'js')
                mock.get('{url}/courses'.format(url=URL), content=b'html')
                mock.get('{url}/styles/app.css'.format(url=URL), content=b'css')
                path_index_page = download(URL, tempdir)
                assert expected_path_index_page == path_index_page

                resources_dir = join(tempdir, 'test-com_files')
                assert isdir(resources_dir)
                expected_files = [
                    'test-com-images-python.png',
                    'test-com-courses.html',
                    'test-com-scripts-test.js',
                    'test-com-styles-app.css',
                    'test-com-images-{name}a.png'.format(
                        name=long_name[:len(long_name) - len('test-com-images-')],
                    ),
                    'test-com-images-{name}0.png'.format(
                        name=long_name[:len(long_name) - len('test-com-images-')],
                    ),
                    'test-com-images-{name}1.png'.format(
                        name=long_name[:len(long_name) - len('test-com-images-')],
                    ),
                ]
                for filename in expected_files:
                    assert isfile(join(resources_dir, filename))

                with open(get_file_absolute_path('expected.html')) as file_exp:
                    with open(path_index_page) as file_tested:
                        assert file_exp.read() == file_tested.read()
