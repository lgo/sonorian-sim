import collections
import sys
import time
import math
import datetime

import importlib

import sonorian.gui.menu_builder as menu_builder
import sonorian.gui.action_bar as action_bar
import sonorian.gui.status as status
import sonorian.world as world

"""
main_menu contains the generated menu.
"""


def round_sigfigs(num, sig_figs):
    """Round to specified number of sigfigs.

    >>> round_sigfigs(0, sig_figs=4)
    0
    >>> int(round_sigfigs(12345, sig_figs=2))
    12000
    >>> int(round_sigfigs(-12345, sig_figs=2))
    -12000
    >>> int(round_sigfigs(1, sig_figs=2))
    1
    >>> '{0:.3}'.format(round_sigfigs(3.1415, sig_figs=2))
    '3.1'
    >>> '{0:.3}'.format(round_sigfigs(-3.1415, sig_figs=2))
    '-3.1'
    >>> '{0:.5}'.format(round_sigfigs(0.00098765, sig_figs=2))
    '0.00099'
    >>> '{0:.6}'.format(round_sigfigs(0.00098765, sig_figs=3))
    '0.000988'
    """
    if num != 0:
        return round(num, -int(math.floor(math.log10(abs(num))) - (sig_figs - 1)))
    else:
        return 0  # Can't take the log of 0


def pretty_elapsed_time(start_time, end_time):
    """
    Returns a pretty representation of the timedelta, in seconds.
    """
    elapsed = end_time - start_time
    return "{0:.3}s".format(round_sigfigs(elapsed, sig_figs=3))

def _generate(window):
    # TODO(joey): A loading spinner would be nice.
    window.action_bar.set_msg('generating world...',
                              status=status.STATUS_ERROR)

    start_time = time.time()
    w = world.World()
    end_time = time.time()

    window.set_world(w)
    window.action_bar.set_msg('generated world. took {time}'.format(time=pretty_elapsed_time(start_time, end_time)),
                              status=status.STATUS_SUCCESS)


def _reload_code(window):
    # TODO(joey): A loading spinner would be nice.
    window.action_bar.set_msg('reloading code...',
                              status=status.STATUS_ERROR)
    start_time = time.time()
    importlib.reload(world)
    window.reload_code()
    end_time = time.time()

    window.action_bar.set_msg('code reloaded. took {time}'.format(time=pretty_elapsed_time(start_time, end_time)),
                              status=status.STATUS_SUCCESS)

def _quit(window):
    sys.exit(0)

def _settings_size(window):
    window.action_bar.set_msg('(would have) set size',
                              status=status.STATUS_OK)


def _settings_probability(window):
    window.action_bar.set_msg('(would have) set probabilities',
                              status=status.STATUS_OK)


def generate_main_menu(gen):
    gen += menu_builder.Action('g', 'generate', _generate)
    gen += menu_builder.Action('r', 'reload code', _reload_code)

    with gen.submenu('s', 'settings'):
        gen += menu_builder.Action('s', 'size', _settings_size)
        gen += menu_builder.Action('p', 'probability', _settings_probability)

    gen += menu_builder.Action('q', 'quit', _quit)

    return gen.finish()
