"""
A simple logger considering a verbosity level.
Simple implementation directory writing to stderr.
Author: Vincenzo Musco (http://www.vmusco.com)
Date: 9 January 2019
"""
import sys

__author__ = "Vincenzo Musco (http://www.vmusco.com)"
__date__ = "9 January 2019"


class VerboseLogger(object):
    """
    A verbose logger printing messages on stderr according of the verbose level
    """

    def __init__(self, max_verbosity: int = 1):
        self._verbosity = 0
        self._max_verbosity = max_verbosity

    def set_verbosity(self, level: int) -> None:
        """
        :param level: new verbosity level (higher = more verbose)
        """
        self._verbosity = min(level, self._max_verbosity)

    def _is_level(self, level: int) -> bool:
        return self._verbosity >= level

    def print_if_level(self, min_level: int, msg: str) -> None:
        """
        Print a message on stderr if the verbosity level is at least of min_level
        :param min_level:
        :param msg:
        """
        if self._is_level(min_level):
            print(msg, file=sys.stderr)


class VerboseObject(object):
    """
    Class representing an object which print verbose debug info on stderr
    """

    def __init__(self):
        self._logger = VerboseLogger(0)

    def set_logger(self, logger: VerboseLogger) -> None:
        """
        Set the logger object
        """
        self._logger = logger
