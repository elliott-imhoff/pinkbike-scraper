"""General utilities."""

import requests
from requests.exceptions import ConnectionError
from retry import retry


@retry(ConnectionError, delay=5, tries=6)
def retry_request(url):
    """Retry wrapper around request to prevent crashes due to connection errors."""
    return requests.get(url)
