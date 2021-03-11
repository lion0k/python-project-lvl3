"""Request module."""

from requests import get
from requests.exceptions import RequestException

ERROR_REQUEST = "\n\nThe page at this address '{url}' was not loaded.\n{error}"
SUCCESSFUL_STATUS_CODE = 200


def send_request(url: str):
    """
    Send request to url.

    Args:
        url: url

    Raises:
        RequestException: error send request

    Returns:
        any:
    """
    try:
        response = get(url)
    except RequestException as error:
        raise RequestException(ERROR_REQUEST.format(url=url, error=error))

    if response.status_code != SUCCESSFUL_STATUS_CODE:
        response.raise_for_status()

    return response.content
