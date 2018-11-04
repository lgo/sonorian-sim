import sys
import curses
import importlib

import sonorian.gui.action_bar as action_bar
import sonorian.gui.menu_builder as menu_builder
import sonorian.gui.status as status
import sonorian.gui.menus.main_menu as main_menu
import sonorian.world as world


import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class MainWindow(object):
    """
    Provides an interactive interface for World using ncurses.
    """

    def __init__(self):
        self._world = None
        self._menu_stack = []

    def loop(self):
        """
        Begin the interactive window.
        """
        try:
            curses.wrapper(self._loop)
        except (SystemExit, KeyboardInterrupt):
            pass

    def _loop(self, stdscr):
        """
        Internal interactive loop. It is executed using curses.wrapper
        to recover terminal settings after execution.
        """
        self.stdscr = stdscr
        self.height, self.width = self.stdscr.getmaxyx()

        # Hide the cursor.
        curses.curs_set(0)

        # Initialize colours.
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

        # Initialize the action bar.
        self.action_bar = action_bar.ActionBar(self.stdscr)
        self.action_bar.redraw()

        # Initialize main menu. It also calls into the action_bar to set
        # the menu.
        self.set_menu(self.main_menu)

        # Start receiving input.
        while True:
            self._input_loop()

    def _input_loop(self):
        """
        Receive input and execute an action.
        """
        ch = self.stdscr.getch()
        # Clear out the action status. If the next action does not
        # produce a message, then it will remain blank.
        self.action_bar.clear_msg()
        if ch == curses.KEY_RESIZE:
            self.call_for_resize()
        elif ch == -1:
            # No input is available. no-op
            pass
        elif self._menu.get(chr(ch)) is not None:
            self._menu.get(chr(ch)).fn()(self)
        else:
            msg = None
            # ch is not always a valid character. For example, negative
            # error codes may be returned.
            if 0 < ch and ch < 0x110000:
                msg = 'invalid key (%d/%c)' % (ch, ch)
            else:
                msg = 'invalid key (%d)' % ch
            self.action_bar.set_msg(msg, status=status.STATUS_ERROR)

    def call_for_resize(self):
        """
        Called when we want to resize the screen.
        """
        (height, width) = self.stdscr.getmaxyx()
        self.redraw_world()
        self.action_bar.resize()
        self.height, self.width = height, width

    def redraw_world(self):
        self.stdscr.clear()

    def set_world(self, world):
        self._world = world
        # TODO(joey): Draw world.

    @property
    def main_menu(self):
        gen = menu_builder.MenuTreeGenerator()
        return main_menu.generate_main_menu(gen)

    def set_menu(self, menu):
        self._menu = menu
        self.action_bar.set_actions(self._menu)

    def menu_back(self):
        # TODO(joey): Check if the menu stack is empty.
        self._menu = self._menu_stack.pop()
        self.action_bar.set_actions(self._menu)

    def menu_enter(self, key):
        item = self._menu.get(key)
        if item is None:
            raise Exception("unexpected error: expected value MenuTree element")
        if not isinstance(item, menu_builder.Submenu):
            raise Exception("unexpected error: expected menu_builder.Submenu")
        self._menu_stack.append(self._menu)
        self._menu = item
        self.action_bar.set_actions(self._menu)


    def reload_code(self):
        importlib.reload(world)
        if self._world is not None:
            dump = self._world.serialize()
            self._world = world.World.from_dump(dump)
