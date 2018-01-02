import collections
import sys
from sonorian.gui.menu_builder import Action, MenuTreeGenerator
from sonorian.gui.action_bar import STATUS_OK

"""
main_menu contains the generated menu.
"""

def _generate(window):
    window.action_bar.set_msg( '(would have) generated world',
    status=STATUS_OK)

def _quit(window):
    sys.exit(0)

def _settings_size(window):
    window.action_bar.set_msg('(would have) set size',
                              status=STATUS_OK)


def _settings_probability(window):
    window.action_bar.set_msg('(would have) set probabilities',
                              status=STATUS_OK)

def generate_main_menu(gen):
    gen += Action('g', 'generate', _generate)

    with gen.submenu('s', 'settings'):
        gen += Action('s', 'size', _settings_size)
        gen += Action('p', 'probability', _settings_probability)

    gen += Action('q', 'quit', _quit)

    return gen.finish()
