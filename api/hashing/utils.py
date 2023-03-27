"""
Hashing Utilities API

This module contains the API for hashing web documents and URLs.
It is used by the Filter API to filter out duplicate content.
"""

# Standard Library
from hashlib import sha256

# Custom Exceptions
# =================
class HashingError(Exception):
    """
    An exception class for hashing errors.
    """

# Functions
# =========
def __digest(content):
    """
    This function returns the SHA256 digest of a string.

    Parameters
    ----------
    content : str
        The content to be hashed.

    Returns
    -------
    str
        The SHA256 digest of a string.
    """
    return sha256(content.encode('utf-8')).hexdigest()

def __digest_gen(content):
    """
    This function returns an iterator to SHA256 digests for strings.

    Parameters
    ----------
    content : iterator
        The content to be hashed.

    Returns
    -------
    iterator
        An iterator to SHA256 digests for strings.
    """
    try:
        for string in content:
            yield sha256(string.encode('utf-8')).hexdigest()
    except:
        raise HashingError('Invalid content type')

def digest(content):
    """
    This function returns the SHA256 digest of a string or an iterator to
    SHA256 digests for strings.

    Parameters
    ----------
    content : str or iterator
        The content to be hashed.

    Raises
    ------
    HashingError
        If the content is not a string or an iterator for strings.

    Returns
    -------
    str or iterator
        The SHA256 digest of a string or an iterator to SHA256 digests for
        strings.
    """
    if isinstance(content, str):
        return __digest(content)

    return __digest_gen(content)
