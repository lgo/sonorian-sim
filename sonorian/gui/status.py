"""
status contains colour statuses.
"""

import curses


# FIXME(joey): Colours are off as my terminal colours are wonky :/
# TODO(joey): Maybe make these enums.
STATUS_SUCCESS = curses.COLOR_BLUE
STATUS_OK = curses.A_NORMAL
STATUS_ERROR = curses.COLOR_YELLOW
