"""
Filter Utilities API

This module provides utility functions for the filter API.
"""

# Hashing Records API
from ..hashing.records import HashRecords

# Custom Exceptions
# =================
class FilterError(Exception):
    """
    An exception class for filter errors.
    """

class FilterBase:
    """
    This class is the base class for all filter classes.
    """
    def __init__(self, history = None, placeholder = None):
        """
        This function initializes the filter class.

        Parameters
        ----------
        history : list
            A list of previously filtered content.
        placeholder : str
            A placeholder for the filtered content.
        """
        self.__history = HashRecords()
        if history and placeholder:
            self.__history[history] = placeholder

    def __call__(self, content):
        """
        This function is the main function for the filter class.

        Parameters
        ----------
        content : str
            The content to be filtered.

        Raises
        ------
        NotImplementedError
            This function is not implemented.

        Returns
        -------
        str
            The filtered content.
        """
        raise NotImplementedError
