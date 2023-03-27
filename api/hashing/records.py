"""
Hashing Records API

This module contains a class for storing the hashes of content.
It is used by the Filter API to filter out duplicate content.
"""

# Hashing Utilities API
from . import utils

class HashRecords:
    """
    HashRecords class

    This class is used to store the hashes of content. And check if the content
    already exists in the records.
    """
    def __init__(self):
        """
        Initialize the HashRecords class
        """
        self.__records = {}

    def __contains__(self, content):
        """
        Check if the content already exists in the records.

        Parameters
        ----------
        content : str
            The content to be checked.

        Returns
        -------
        bool
            True if the content already exists in the records, False otherwise.
        """
        if isinstance(content, str):
            return utils.digest(content) in self.__records
        else:
            False

    def __setitem__(self, content, placeholder = None):
        """
        Add the content to the records.

        Parameters
        ----------
        content : str or iterator
            The content to be added.
        placeholder : any, optional
            A placeholder for the content. The default is None.
        """
        if isinstance(content, str):
            self.__records[utils.digest(content)] = placeholder
        else:
            for key, value in zip(utils.digest(content), placeholder):
                self.__records[key] = value

    def __delitem__(self, content):
        """
        Remove the content from the records.

        Parameters
        ----------
        content : str or iterator
            The content to be removed.
        """
        if isinstance(content, str):
            del self.__records[utils.digest(content)]
        else:
            for key in utils.digest(content):
                del self.__records[key]

    def __len__(self):
        """
        Get the number of records.

        Returns
        -------
        int
            The number of records.
        """
        return len(self.__records)

    def __rsub__(self, content):
        """
        Return the entries not in records

        Parameters
        ----------
        content : str or iterator
            The content to be checked.

        Returns
        -------
        generator
            The entries not in records.
        """
        if isinstance(content, str):
            if utils.digest(content) not in self.__records:
                yield content
            return

        for key, value in zip(utils.digest(content), content):
            if key not in self.__records:
                yield value

