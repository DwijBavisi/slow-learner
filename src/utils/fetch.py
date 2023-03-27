"""
Fetching utilities

This module contains utilities for fetching web pages and extracting links from them.
"""

# File handling
from urllib.parse import urljoin

# Parsing
import re
from bs4 import BeautifulSoup

# HTTP requests
import requests

# Fingerprinting
from . import fingerprint as fp

__RELATIVE = re.compile(r'^[./]+')
__ARGS = re.compile(r'[?#].*$')

class FetchError(Exception):
    """
    This class is used to raise an exception when a web page cannot be fetched.
    Or has already been fetched earlier.
    """
    def __init__(self, url: str, message: str = 'Unable to fetch '):
        """
        This function initializes the exception.
        """
        self.url = url
        self.message = message
        super().__init__(self.message + self.url)

class ParseError(FetchError):
    """
    This class is used to raise an exception when a web page cannot be parsed.
    Or has already been parsed earlier.
    """
    def __init__(self, url: str, message: str = 'Unable to parse '):
        """
        This function initializes the exception.
        """
        super().__init__(url, message)

def __fetch(url: str) -> str:
    """
    Fetches a web page

    Parameters
    ----------
    url : str
        The URL of the web page to fetch

    Returns
    -------
    str
        The HTML of the web page
    """
    with requests.Session() as session:
        return session.get(url).text

def __parse(text: str, url: str, parser: str = 'html.parser') -> BeautifulSoup:
    """
    Parses a web page using BeautifulSoup

    Parameters
    ----------
    text : str
        The conent of the web page to fetch
    url : str
        The URL of the web page
    parser : str, optional
        The parser to use, by default 'html.parser'

    Returns
    -------
    BeautifulSoup
        The parsed web page
    """
    soup = BeautifulSoup(text, parser)
    for link in soup.find_all('a', href = True):
        path = __ARGS.sub('', link.get('href'))
        if path and __RELATIVE.match(path):
            path = urljoin(url, path)
        yield path

def fetch(url: str, check: bool = True) -> str:
    """
    Fetches a web page

    Parameters
    ----------
    url : str
        The URL of the web page to fetch
    check : bool, optional
        Whether to check if the URL has already been fetched, by default True

    Returns
    -------
    str
        The HTML of the web page
    """
    if check and fp.exists(url):
        raise FetchError(url)

    text = __fetch(url)
    fp.add(url)

    return text

def parse(url: str, text: str = None, check: bool = True) -> BeautifulSoup:
    """
    Parses a web page using BeautifulSoup

    Parameters
    ----------
    url : str
        The URL of the web page to fetch
    text : str, optional
        The conent of the web page to parse
    check : bool, optional
        Whether to check if the URL has already been fetched, by default True

    Returns
    -------
    BeautifulSoup
        The parsed web page
    """
    if text is None:
        text = fetch(url, check)

    if check and fp.exists(text, fp.DOCTYPE):
        raise ParseError(url)

    parsed = __parse(text, url)
    fp.add(text, url, fp.DOCTYPE)

    return parsed
