"""
Fingerprinting utilities

This module contains utilities for fingerprinting URLs and documents.
It uses the fingerprint.json file to store the fingerprints of URLs and documents.
"""

# Data handling
import json

# File handling
from os import path
from os.path import join
from os.path import abspath

# Hashing
from hashlib import md5

# File path to the fingerprint.json file
__DIRNAME = abspath(path.dirname(__file__))
__FPJSON = join(__DIRNAME, '../../assets/fingerprint.json')
__SAMPLE = join(__DIRNAME, '../../assets/sample/fingerprint.sample.json')

# In-memory version of the fingerprint.json file
__FPMEM = None

# Types
URLTYPE = 'url'
DOCTYPE = 'doc'

# Set encoder
# Encodes sets as lists so they can be serialized to JSON
class SetEnc(json.JSONEncoder):
    """
    Encodes sets as lists so they can be serialized to JSON
    """
    def default(self, o):
        """
        Encodes sets as lists

        Parameters
        ----------
        o : set
            The set to encode

        Returns
        -------
        list
            The encoded set
        """
        if isinstance(o, set):
            return list(o)
        return json.JSONEncoder.default(self, o)

def get_hash(text: str) -> str:
    """
    Hashes a string using MD5

    Parameters
    ----------
    text : str
        The string to key

    Returns
    -------
    str
        The hashed string
    """
    return md5(text.encode('utf-8')).hexdigest()

def __load() -> dict:
    """
    Loads the fingerprint.json file into memory

    Returns
    -------
    dict
        The fingerprint.json file
    """
    if path.exists(__FPJSON):
        with open(__FPJSON, 'r', encoding = 'UTF-8') as file:
            return json.load(file)
    else:
        with open(__SAMPLE, 'r', encoding = 'UTF-8') as file:
            return json.load(file)

def save() -> None:
    """
    Saves the in-memory version of the fingerprint.json file to disk
    """
    if not __FPMEM:
        init()
    with open(__FPJSON, 'w', encoding = 'UTF-8') as file:
        json.dump(__FPMEM, file, indent = 4, cls = SetEnc)

def __exists(key: str, value: str, cat: str = URLTYPE) -> bool:
    """
    Checks if a key exists in the fingerprint.json file

    Parameters
    ----------
    key : str
        The key to check
    value : str
        The URL to check
    cat : str, optional
        The category of key to check, by default URLTYPE

    Returns
    -------
    bool
        True if the URL exists in the fingerprint.json file, False otherwise
    """
    if not __FPMEM:
        init()
    if cat in __FPMEM:
        if key in __FPMEM[cat]:
            return cat == DOCTYPE or value in __FPMEM[cat][key]
        return False
    raise ValueError(f'Invalid category \'{cat}\'')

def exists(value: str, cat: str = URLTYPE) -> bool:
    """
    Checks if a URL/DOC exists in the fingerprint.json file

    Parameters
    ----------
    value : str
        The URL/DOC to check
    cat : str, optional
        The category of key to check, by default URLTYPE

    Returns
    -------
    bool
        True if the URL exists in the fingerprint.json file, False otherwise
    """
    return __exists(get_hash(value), value, cat)

def __add(key: str, value: str, cat: str = URLTYPE) -> None:
    """
    Adds a key to the fingerprint.json file

    Parameters
    ----------
    key : str
        The key to add
    value : str
        The URL to add
    cat : str, optional
        The category of key to add, by default URLTYPE
    """
    if not __FPMEM:
        init()
    if __exists(key, value, cat):
        return

    if not key in __FPMEM[cat]:
        __FPMEM[cat][key] = set()
    if isinstance(__FPMEM[cat][key], list):
        __FPMEM[cat][key] = set(__FPMEM[cat][key])
    __FPMEM[cat][key].add(value)

def add(value: str, url: str = None, cat: str = URLTYPE) -> None:
    """
    Adds a URL/DOC to the fingerprint.json file

    Parameters
    ----------
    value : str
        The URL/DOC to add
    url : str, optional
        The URL to add, by default None
    cat : str, optional
        The category of key to add, by default URLTYPE
    """
    __add(get_hash(value), value if cat == URLTYPE else url, cat)

def init() -> None:
    """
    Initializes the in-memory version of the fingerprint.json file
    """
    global __FPMEM
    __FPMEM = __load()
