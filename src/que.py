"""
Queue handling

This module handles the queue of the learner. It is responsible for
loading the queue from the queue.json file, and saving it back to the
same file. It also provides the deq() function which returns the next
batch of documents to be learned.
"""

# Data handling
import json

# File handling
from os import path
from os.path import join
from os.path import abspath
from urllib.parse import urlparse
import urllib.robotparser as urobot

# Data structures
from collections import deque

# Local imports
from .utils import fetch as fc
from .utils import fingerprint as fp

# File path to the queue.json and config.json file
__DIRNAME = abspath(path.dirname(__file__))
__QJSON = join(__DIRNAME, '../assets/queue.json')
__QSAMPLE = join(__DIRNAME, '../assets/sample/queue.sample.json')
__CJSON = join(__DIRNAME, '../assets/config.json')
__CSAMPLE = join(__DIRNAME, '../assets/sample/config.sample.json')

# In-memory queue
__QUE = None

class QueEnc(json.JSONEncoder):
    """
    This class is used to encode the queue to JSON. It is used to
    convert the deque to a list before encoding.
    """
    def default(self, o):
        """
        This function is called by the JSON encoder when it encounters
        an object it does not know how to encode. In this case, it
        converts the deque to a list.
        """
        if isinstance(o, deque):
            return list(o)
        return json.JSONEncoder.default(self, o)

def __load_que() -> dict:
    """
    This function loads the queue from the queue.json file. If the
    file does not exist, it loads the sample queue instead.

    Returns
    -------
    dict
        The queue
    """
    if path.exists(__QJSON):
        with open(__QJSON,'r', encoding = 'UTF-8') as file:
            return json.load(file)
    else:
        with open(__QSAMPLE, 'r', encoding = 'UTF-8') as file:
            return json.load(file)

def __load_conf() -> dict:
    """
    This function loads the configuration from the config.json file.

    Returns
    -------
    dict
        The configuration
    """
    if path.exists(__CJSON):
        with open(__CJSON,'r', encoding = 'UTF-8') as file:
            return json.load(file)
    else:
        with open(__CSAMPLE, 'r', encoding = 'UTF-8') as file:
            return json.load(file)

def __load() -> None:
    """
    This function loads the queue and configuration from the files.
    """
    global __QUE

    __QUE = __load_que()

    if len(__QUE['queue']) == 0:
        __QUE = __load_conf()

        __QUE['queue'] = __QUE['seeds']
        del __QUE['seeds']

def enq(link: str) -> None:
    """
    This function adds a link to the queue.

    Parameters
    ----------
    link : str
        The URL of the link to add
    """
    if __QUE is None:
        init()
    __QUE['queue'].append(link)

def __popleft() -> str:
    """
    This function removes the first element from the queue.

    Returns
    -------
    str
        The URL of the removed element
    """
    if __QUE is None:
        init()

    if len(__QUE['queue']) == 0:
        return False
    return __QUE['queue'].popleft()

def deq(cnt: int = 10) -> str:
    """
    This function returns the next document to be learned.

    Parameters
    ----------
    cnt : int, optional
        The number of documents to return, by default 10
    """
    if __QUE is None:
        init()

    while (url := __popleft()) and (cnt > 0):
        try:
            text = fc.fetch(url)
            outlinks = fc.parse(url, text)
        except (fc.FetchError, fc.ParseError):
            continue

        cnt -= 1

        rp = urobot.RobotFileParser()
        rp.set_url("https://" + urlparse(url).netloc + "/robots.txt")
        rp.read()

        # print(rp, "https://" + urlparse(url).netloc + "/robots.txt")

        for outlink in outlinks:
            if not fp.exists(outlink):
                if rp.can_fetch("*", outlink):
                    enq(outlink)
                    # fp.add(outlink)
                else:
                    print("Blocked by robots.txt:", outlink)
        yield text
    save()

def save() -> None:
    """
    This function saves the queue to the queue.json file.
    """
    if __QUE is None:
        init()
    with open(__QJSON, mode = 'w', encoding = 'UTF-8') as file:
        json.dump(__QUE, file, indent = 4, cls = QueEnc)
    fp.save()

def init() -> None:
    """
    This function initializes the queue.
    """
    __load()
    __QUE['queue'] = deque(__QUE['queue'])

